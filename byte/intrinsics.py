from typing import Any, Callable, cast, TypeAlias
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from byte.llvm_extensions import llint, IRBuilderExt, ModuleExt
from byte import ast


IntrinsicPyFunc: TypeAlias = Callable[['IntrinsicCallContext'], Any]

@dataclass
class IntrinsicCallContext:
    pos: ast.Position
    builder: IRBuilderExt
    module: ModuleExt
    file: ast.File
    name: str
    codegen: Any
    args: list[ast.Arg] = field(default_factory=list)
    codegen_args: list[Any] = field(default_factory=list)

    def arg(self, idx: int):
        return self.codegen_args[idx]

    def error_literal(self, msg: str):
        string_type = self.module.context.get_identified_type('string')
        global_var = self.module.global_string(msg, 'oom_global')
        err_var_ptr = self.builder.first_elem(global_var, 'oom_ptr')
        err_string = self.builder.struct(string_type, [err_var_ptr, llint(len(msg))], 'oom_string')
        return self.call('error', [ast.Arg(self.pos, self.file.type_map.get('string'), err_string)])

    def call(self, name: str, args: list[ast.Arg] | None = None):
        return self.codegen.call(self.pos, name, args or [])

def intrinsic(
    self, ret_type: ast.Type | None = None, params: list[ast.Param] | None = None, flags: ast.FunctionFlags | None = None,
    override_name: str | None = None
):
    if ret_type is None:
        ret_type = self.file.type_map.get('nil')

    if params is None:
        params = []

    if flags is None:
        flags = ast.FunctionFlags()

    def decorator(func: IntrinsicPyFunc):
        name = override_name or func.__name__[1:]
        ast_func = ast.Function(ast.Position(), cast(ast.Type, ret_type), name, params, func, flags)
        setattr(func, 'ast_func', ast_func)

        if self is not None:
            self.intrinsics[name] = func
        
        return func

    return decorator

def intrinsic_op(self, op: str, ret_type: ast.Type, a_type: ast.Type, b_type: ast.Type | None = None):
    if b_type is None:
        name = f'{op}.{a_type}'
        params = [ast.Param(ast.Position(), a_type, 'a')]
    else:
        name = f'{op}.{a_type}.{b_type}'
        params = [ast.Param(ast.Position(), a_type, 'a'), ast.Param(ast.Position(), b_type, 'b')]

    return intrinsic(self, ret_type, params, override_name=name)

class IntrinsicLib(ABC):
    def __init__(self, file: ast.File):
        self.intrinsics = {}
        self.file = file

    @abstractmethod
    def init(self):
        ...

class IntrinsicClass(IntrinsicLib):
    ...
