from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicCallContext, get_ast_funcs
from byte.llvm_extensions import NULL, llint
from byte import ast


def define_array(file: ast.File, T: ast.Type, size: int | None = None):
    if size is None:
        raise NotImplementedError('dynamic arrays')
    
    arr_type = ast.ArrayType(T, size)
    file.type_map.add(str(arr_type), arr_type)
    array_methods = []

    int_type = file.type_map.get('int')
    string_type = file.type_map.get('string')
    bool_type = file.type_map.get('bool')
    nil_type = file.type_map.get('nil')
    pointer_type = file.type_map.get('pointer')
    StringBuilder_type = file.type_map.get('StringBuilder')
    
    @intrinsic(array_methods, arr_type, override_name=f'{arr_type}.new')
    def array_new(ctx: IntrinsicCallContext):
        malloc = ctx.module.registry.get('malloc')
        
        code_type = ctx.module.context.get_identified_type(str(arr_type))
        elem_type = ctx.codegen.visit(T)
        elem_size = ctx.module.sizeof(elem_type)
        elements_size = ctx.builder.mul(elem_size, llint(size), 'elements_size')
        elements_raw_ptr = ctx.builder.call(malloc, [elements_size], 'elements_raw_ptr')
        elements_raw_ptr_is_null = ctx.builder.icmp_signed('==', elements_raw_ptr, NULL(), 'elements_raw_ptr_is_null')
        with ctx.builder.if_then(elements_raw_ptr_is_null):
            ctx.error_literal('out of memory')
        
        elements_ptr = ctx.builder.bitcast(elements_raw_ptr, ir.PointerType(elem_type), 'elements_ptr')
        return ctx.builder.struct(code_type, [elements_ptr, llint(0)], ctx.name)

    @intrinsic(
        array_methods, nil_type, [ast.Param(ast.Position(), arr_type.reference(), 'self')],
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
        array_methods, int_type, [ast.Param(ast.Position(), arr_type, 'self')],
        flags=ast.FunctionFlags(property=True), override_name=f'{arr_type}.length'
    )
    def array_length(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)
        return ctx.builder.extract_value(struct, 1, 'length')

    @intrinsic(
        array_methods, string_type, [ast.Param(ast.Position(), arr_type, 'self')],
        flags=ast.FunctionFlags(method=True), override_name=f'{arr_type}.to_string'
    )
    def array_to_string(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)

        length = ctx.builder.extract_value(struct, 1, 'length')

        def str_lit(text: str):
            text_global = ctx.module.global_string(text)
            return ctx.call('string.new', [
                ast.Arg(ctx.pos, pointer_type, ctx.builder.first_elem(text_global, 'ptr')),
                ast.Arg(ctx.pos, int_type, llint(len(text))),
                ast.Arg(ctx.pos, bool_type, llint(0, 1))
            ])

        sb = ctx.call('StringBuilder.new', [ast.Arg(ctx.pos, int_type, llint(25))])
        sb_ptr = ctx.builder.allocate_value(sb, 'sb.ptr')
        ctx.call('StringBuilder.add', [
            ast.Arg(ctx.pos, StringBuilder_type.reference(), sb_ptr),
            ast.Arg(ctx.pos, string_type, str_lit('['))
        ])

        i_ptr = ctx.builder.allocate_value(llint(0), 'i.ptr')
        with ctx.builder.while_() as (test, body):
            with test as (_, block1, block2):
                i = ctx.builder.load(i_ptr, 'i')
                cmp = ctx.builder.icmp_signed('<', i, length, 'cmp')
                ctx.builder.cbranch(cmp, block1, block2)

            with body:
                i = ctx.builder.load(i_ptr, 'i')
                element = ctx.call(f'{arr_type}.get', [
                    ast.Arg(ctx.pos, arr_type, struct),
                    ast.Arg(ctx.pos, int_type, i)
                ])

                element_str = ctx.call(f'{T}.to_string', [ast.Arg(ctx.pos, T, element)])
                ctx.call('StringBuilder.add', [
                    ast.Arg(ctx.pos, StringBuilder_type.reference(), sb_ptr),
                    ast.Arg(ctx.pos, string_type, element_str)
                ])

                num_commas = ctx.builder.sub(length, llint(1), 'num_commas')
                needs_comma = ctx.builder.icmp_signed('<', i, num_commas, 'needs_comma')
                with ctx.builder.if_then(needs_comma):
                    ctx.call('StringBuilder.add', [
                        ast.Arg(ctx.pos, StringBuilder_type.reference(), sb_ptr),
                        ast.Arg(ctx.pos, string_type, str_lit(', '))
                    ])

                i_inc = ctx.builder.add(i, llint(1), 'i.inc')
                ctx.builder.store(i_inc, i_ptr)

        ctx.call('StringBuilder.add', [
            ast.Arg(ctx.pos, StringBuilder_type.reference(), sb_ptr),
            ast.Arg(ctx.pos, string_type, str_lit(']'))
        ])

        sb = ctx.builder.load(sb_ptr, 'sb')
        buf = ctx.call('StringBuilder.to_string', [ast.Arg(ctx.pos, StringBuilder_type, sb)])
        ctx.call('StringBuilder.destroy', [ast.Arg(ctx.pos, StringBuilder_type.reference(), sb_ptr)])
        return buf

    @intrinsic(
        array_methods, T, [ast.Param(ast.Position(), arr_type, 'self'), ast.Param(ast.Position(), int_type, 'idx')],
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
