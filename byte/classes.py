from typing import cast

from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicCallContext
from byte.llvm_extensions import llint, NULL
from byte import ast


def init_field(file: ast.File, cls_type: ast.ClassType, i: int, field: ast.Property):
    self_param = ast.Param(field.pos, cls_type, 'self')
    @intrinsic(
        None, field.type, [self_param], flags=ast.FunctionFlags(property=True, returns_reference=True),
        override_name=f'{cls_type}.{field.name}'
    )
    def getter(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)
        if isinstance(struct.type, ir.PointerType): # TODO: feels like a hacky fix
            field_ptr = ctx.builder.extract_ptr(struct, i, f'{field.name}.ptr')
            return ctx.builder.load(field_ptr, field.name)

        return ctx.builder.extract_value(struct, i, field.name)

    field_get = getattr(getter, 'ast_func')

    self_ref_param = ast.Param(field.pos, cls_type.reference(), 'self')
    set_params = [self_ref_param, ast.Param(field.pos, field.type, 'value')]
    @intrinsic(
        None, file.type_map.get('nil'), set_params, flags=ast.FunctionFlags(method=True),
        override_name=f'{cls_type}.set.{field.name}'
    )
    def setter(ctx: IntrinsicCallContext):
        struct = ctx.arg(0)
        value = ctx.arg(1)
        field_ptr = ctx.builder.extract_ptr(struct, i, f'{field.name}.ptr')
        ctx.builder.store(value, field_ptr)

    field_set = getattr(setter, 'ast_func')
    return field_get, field_set

def init_class(pos: ast.Position, file: ast.File, name: str, fields: list[ast.Property]):
    field_types = [field.type for field in fields]
    cls_type = cast(ast.ClassType, file.type_map.add(name, ast.ClassType(name, field_types)))

    constructor_params = [ast.Param(pos, member.type, member.name, ast.ParamFlags(copy=True)) for member in fields]
    @intrinsic(
        None, cls_type, constructor_params, flags=ast.FunctionFlags(static=True, method=True),
        override_name=f'{cls_type}.new'
    )
    def constructor(ctx: IntrinsicCallContext):
        struct_type = ctx.codegen.visit(cls_type)
        return ctx.builder.struct(struct_type, ctx.codegen_args, ctx.name)

    new_constructor = getattr(constructor, 'ast_func')

    destructor_params = [ast.Param(pos, cls_type.reference(), 'self')]
    @intrinsic(
        None, file.type_map.get('nil'), destructor_params, flags=ast.FunctionFlags(method=True),
        override_name=f'{cls_type}.destroy'
    )
    def destructor(ctx: IntrinsicCallContext):
        struct_ptr = ctx.arg(0)
        for i, field in enumerate(fields):
            field_destructor_name = f'{field.type}.destroy'
            if not file.scope.symbol_table.has(field_destructor_name):
                continue

            field_value = ctx.builder.extract_ptr(struct_ptr, i, f'{field.name}.ptr')
            ctx.call(field_destructor_name, [ast.Arg(ctx.pos, field.type.reference(), field_value)])

    destroy = getattr(destructor, 'ast_func')
    
    field_properties = []
    for i, field in enumerate(fields):
        field_properties.extend(init_field(file, cls_type, i, field))

    string_type = file.type_map.get('string')
    string_format = f'{name}(' + ', '.join(f'{field.name}=%.*s' for field in fields) + ')'
    
    @intrinsic(
        None, string_type, [ast.Param(pos, cls_type, 'self')], flags=ast.FunctionFlags(method=True),
        override_name=f'{cls_type}.to_string'
    )
    def cls_to_string(ctx: IntrinsicCallContext):
        from llvmlite import ir
        
        asprintf = ctx.module.registry.get('asprintf')

        struct = ctx.arg(0)
        field_strs = []
        for i, field in enumerate(fields):
            field_value = ctx.builder.extract_value(struct, i, field.name)
            field_str = ctx.call(f'{field.type}.to_string', [ast.Arg(ctx.pos, field.type, field_value)])
            field_strs.append(field_str)

        buf_addr = ctx.builder.alloca(ir.PointerType(ir.IntType(8)), name='buf.addr')
        ctx.builder.store(NULL(), buf_addr)

        fmt = ctx.module.try_get_global(
            f'{name}_str_fmt', lambda: ctx.module.global_string(string_format, f'{name}_str_fmt')
        )
        fmt_ptr = ctx.builder.first_elem(fmt, 'fmt_ptr')

        asprintf_args = [buf_addr, fmt_ptr]
        for field_str in field_strs:
            length = ctx.call('string.length', [ast.Arg(ctx.pos, ctx.file.type_map.get('string'), field_str)])
            ptr = ctx.call('string.ptr', [ast.Arg(ctx.pos, ctx.file.type_map.get('string'), field_str)])
            asprintf_args.append(length)
            asprintf_args.append(ptr)

        written = ctx.builder.call(asprintf, asprintf_args, 'written')
        return ctx.call('string.new', [
            ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), ctx.builder.load(buf_addr, 'buf')),
            ast.Arg(ctx.pos, ctx.file.type_map.get('int'), written),
            ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(1, 1))
        ])

    to_string = getattr(cls_to_string, 'ast_func')
    return [new_constructor, destroy, to_string] + field_properties
