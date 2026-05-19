from dataclasses import dataclass

from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicCallContext, get_ast_funcs
from byte import ast


@dataclass(**ast.NODE_KWARGS)
class ImmutableArrayType(ast.ArrayType):
    def __str__(self) -> str:
        return f'immutable_{super().__str__()}'

# immutable arrays will be a wrapper around llvmlite.ir.VectorType
def define_immutable_array(file: ast.File, T: ast.Type, size: int):
    arr_type = ImmutableArrayType(T, size)
    file.type_map.add(str(arr_type), arr_type)
    array_methods = []
    
    @intrinsic(array_methods, arr_type, flags=ast.FunctionFlags(static=True, method=True), override_name=f'{arr_type}.new')
    def iarray_new(ctx: IntrinsicCallContext):
        elem_type = ctx.codegen.visit(T)
        vec_type = ir.VectorType(elem_type, size)
        return ir.Constant(vec_type, None)

    return arr_type, get_ast_funcs(array_methods)
