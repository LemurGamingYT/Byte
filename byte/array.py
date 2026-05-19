from typing import cast

from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicCallContext, get_ast_funcs
from byte.llvm_extensions import llint
from byte import ast


def define_array(file: ast.File, T: ast.Type, size: int | None = None):
    if size is None:
        raise NotImplementedError('dynamic arrays')
    
    arr_type = ast.ArrayType(T, size)
    file.type_map.add(str(arr_type), arr_type)
    array_methods = []

    nil_type = file.type_map.get('nil')
    
    @intrinsic(array_methods, arr_type, override_name=f'{arr_type}.new')
    def array_new(ctx: IntrinsicCallContext):
        malloc = ctx.module.registry.get('malloc')
        
        code_type = ctx.module.context.get_identified_type(str(arr_type))
        elem_type = ctx.codegen.visit(T)
        elem_size = ctx.module.sizeof(elem_type)
        elements_size = ctx.builder.mul(elem_size, llint(size), 'elements_size')
        elements_raw_ptr = ctx.builder.call(malloc, [elements_size], 'elements_raw_ptr')
        # TODO: check if NULL
        
        elements_ptr = ctx.builder.bitcast(elements_raw_ptr, ir.PointerType(elem_type), 'elements_ptr')
        return ctx.builder.struct(code_type, [elements_ptr, llint(0)], ctx.name)

    @intrinsic(
        array_methods, file.type_map.get('nil'), [ast.Param(ast.Position(), arr_type.reference(), 'self')],
        flags=ast.FunctionFlags(method=True), override_name=f'{arr_type}.destroy'
    )
    def array_destroy(ctx: IntrinsicCallContext):
        free = ctx.module.registry.get('free')
        
        struct = ctx.arg(0)
        
        elements_ptr = ctx.builder.extract_ptr(struct, 0, 'elements_ptr')
        elements_T_ptr = ctx.builder.load(elements_ptr, 'elements_T_ptr')
        elements_i8_ptr = ctx.builder.bitcast(elements_T_ptr, ir.PointerType(ir.IntType(8)), 'elements_i8_ptr')
        ctx.builder.call(free, [elements_i8_ptr])

    @intrinsic(
        array_methods, file.type_map.get('int'), [ast.Param(ast.Position(), arr_type, 'self')],
        flags=ast.FunctionFlags(property=True), override_name=f'{arr_type}.length'
    )
    def array_length(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)
        return ctx.builder.extract_value(struct, 1, 'length')

    @intrinsic(
        None, file.type_map.get('string'), [ast.Param(ast.Position(), arr_type, 'self')],
        flags=ast.FunctionFlags(method=True), override_name=f'{arr_type}.to_string'
    )
    def array_to_string(ctx: IntrinsicCallContext):
        malloc = ctx.module.registry.get('malloc')
        # memcpy = ctx.module.registry.get('memcpy')
        printf = ctx.module.registry.get('printf')

        struct = ctx.arg(0)

        # elements = ctx.builder.extract_value(struct, 0, 'elements')
        length = ctx.builder.extract_value(struct, 1, 'length')

        static_size = 2 # '[' and ']'
        length_is_zero = ctx.builder.icmp_signed('==', length, llint(0), 'length_is_zero')
        string_buf_size_ptr = ctx.builder.alloca(ir.IntType(32), name='string_buf_size_ptr')
        with ctx.builder.if_else(length_is_zero) as (then, else_):
            with then:
                ctx.builder.store(llint(static_size), string_buf_size_ptr)

            with else_:
                length_size = ctx.builder.mul(length, llint(2), 'length_size') # each element has '%s'
                # each element has a comma after it, except for the last one
                num_commas = ctx.builder.sub(length, llint(1), 'num_commas')
                comma_size = ctx.builder.mul(num_commas, llint(2), 'comma_size') # commas have spaces after them
                elements_size = ctx.builder.add(length_size, comma_size, 'elements_size')
                ctx.builder.store(ctx.builder.add(llint(static_size), elements_size, 'string_buf_size'), string_buf_size_ptr)
        
        string_buf_size = ctx.builder.load(string_buf_size_ptr, 'string_buf_size')
        ctx.builder.call(printf, [ctx.builder.first_elem(ctx.module.global_string('%d\n')), string_buf_size])
        
        string_buf_ptr = ctx.builder.call(malloc, [string_buf_size], 'string_buf_ptr')
        # TODO: check if NULL

        func = cast(ir.Function, ctx.builder.function)
        cond_block = func.append_basic_block('while_cond_block')
        body_block = func.append_basic_block('while_body_block')
        merge_block = func.append_basic_block('while_merge_block')

        i_ptr = ctx.builder.allocate_value(llint(0), 'i_ptr')

        ctx.builder.branch(cond_block)
        ctx.builder.position_at_end(cond_block)
        i = ctx.builder.load(i_ptr, 'i')
        cond = ctx.builder.icmp_signed('<', i, length, 'cond')
        ctx.builder.cbranch(cond, body_block, merge_block)

        ctx.builder.position_at_end(body_block)
        i = ctx.builder.load(i_ptr, 'i')

        i_inc = ctx.builder.add(i, llint(1), 'i_inc')
        ctx.builder.store(i_inc, i_ptr)
        ctx.builder.branch(cond_block)
        ctx.builder.position_at_end(merge_block)

        return ctx.call('string.new', [
            ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), string_buf_ptr),
            ast.Arg(ctx.pos, ctx.file.type_map.get('int'), string_buf_size),
            ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(1, 1))
        ])

    @intrinsic(
        array_methods, T, [ast.Param(ast.Position(), arr_type, 'self'), ast.Param(ast.Position(), file.type_map.get('int'), 'idx')],
        flags=ast.FunctionFlags(method=True), override_name=f'{arr_type}.get'
    )
    def array_get(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)
        idx = ctx.arg(1)
        
        elements = ctx.builder.extract_value(struct, 0, 'elements')
        length = ctx.builder.extract_value(struct, 1, 'length')
        idx_ptr = ctx.builder.allocate_value(idx, 'length_ptr')
        idx_is_negative = ctx.builder.icmp_signed('<', idx, llint(0), 'idx_is_negative')
        with ctx.builder.if_then(idx_is_negative):
            ctx.builder.store(ctx.builder.add(length, idx, 'wrap_around_idx'), idx_ptr)

        idx = ctx.builder.load(idx_ptr, 'length')
        length_bounds_check = ctx.builder.icmp_signed('>=', idx, length, 'length_bounds_check')
        with ctx.builder.if_then(length_bounds_check):
            ctx.error_literal('array index out of bounds')

        element_ptr = ctx.builder.gep(elements, [idx], True, 'element_ptr')
        return ctx.builder.load(element_ptr, 'element')

    @intrinsic(
        array_methods, nil_type, [ast.Param(ast.Position(), arr_type.reference(), 'self'), ast.Param(ast.Position(), T, 'x')],
        flags=ast.FunctionFlags(method=True), override_name=f'{arr_type}.add'
    )
    def array_add(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)
        x = ctx.arg(1)

        elements_ptr = ctx.builder.extract_ptr(struct, 0, 'elements')
        length_ptr = ctx.builder.extract_ptr(struct, 1, 'length')

        elements = ctx.builder.load(elements_ptr, 'elements')
        length = ctx.builder.load(length_ptr, 'length')
        capacity_reached = ctx.builder.icmp_signed('>=', length, llint(size), 'capacity_reached')
        with ctx.builder.if_then(capacity_reached):
            ctx.error_literal('array capacity reached')
        
        last_element_ptr = ctx.builder.gep(elements, [length], True, 'last_element_ptr')
        ctx.builder.store(x, last_element_ptr)

        length_inc = ctx.builder.add(length, llint(1), 'length_inc')
        ctx.builder.store(length_inc, length_ptr)

    return arr_type, get_ast_funcs(array_methods)
