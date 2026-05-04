from typing import Any, Callable, cast, TypeAlias
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from logging import info

from byte.llvm_extensions import llint, NULL, IRBuilderExt, ModuleExt, Registry
from byte import ast


IntrinsicPyFunc: TypeAlias = Callable[['IntrinsicCallContext'], Any]

@dataclass
class IntrinsicCallContext:
    pos: ast.Position
    builder: IRBuilderExt
    module: ModuleExt
    name: str
    args: list[Any] = field(default_factory=list)

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

class Intrinsics:
    def __init__(self, file: ast.File):
        self.registered = {}
        self.file = file
    
    def register(self):
        string_type = self.file.type_map.get('string')
        System_type = self.file.type_map.get('System')
        
        self.declare_attribute_function(string_type, 'to_string', string_type)
        
        self.declare_attribute_function(System_type, 'os', string_type, is_static=True, is_method=False)
        
        for definition in Registry.get_all_definitions():
            name = definition.display_name or definition.llvm_name
            param_types = [ast.Type.from_llvm(self.file, ir_type) for ir_type in definition.type.args]
            params = [ast.Param(ast.Position(), type, str(i)) for i, type in enumerate(param_types)]
            ret_type = ast.Type.from_llvm(self.file, definition.type.return_type)
            self.declare_empty_function(name, ret_type, params)
    
    def declare_op_function(
        self, op: str, ret_type: ast.Type, a_type: ast.Type, b_type: ast.Type | None = None, public: bool = True
    ):
        if b_type is None:
            name = f'{op}.{a_type}'
            params = [ast.Param(ast.Position(), a_type, 'a')]
        else:
            name = f'{op}.{a_type}.{b_type}'
            params = [ast.Param(ast.Position(), a_type, 'a'), ast.Param(ast.Position(), b_type, 'b')]
        
        self.declare_empty_function(name, ret_type, params, public=public)
    
    def declare_attribute_function(self, object_type: ast.Type, attr_name: str,
        ret_type: ast.Type | None = None, params: list[ast.Param] | None = None,
        is_static: bool = False, is_method: bool = True, public: bool = True):
        if params is None:
            params = []
        
        if not is_static:
            params.insert(0, ast.Param(ast.Position(), object_type, 'self'))
        
        flags = ast.FunctionFlags(static=is_static, property=not is_method, method=is_method)
        self.declare_empty_function(f'{object_type}.{attr_name}', ret_type, params, flags, public)
    
    def declare_empty_function(self, name: str, ret_type: ast.Type | None = None, params: list[ast.Param] | None = None,
        flags: ast.FunctionFlags | None = None, public: bool = False):
        if flags is None:
            flags = ast.FunctionFlags()
        
        if params is None:
            params = []
        
        if ret_type is None:
            ret_type = self.file.type_map.get('nil')
        
        func = ast.Function(ast.Position(), ret_type, name, params, flags=flags)
        self.file.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func, public=public))
        self.registered[name] = func
    
    def call(self, ctx: IntrinsicCallContext):
        name = ctx.name
        module = ctx.module
        builder = ctx.builder
        args = ctx.args
        pos = ctx.pos
        string_type = module.context.get_identified_type('string')
        
        info(f'calling intrinsic function {name} with {len(args)} arguments')
        match name:
            case 'string.to_string':
                malloc = module.registry.get('malloc')
                memcpy = module.registry.get('memcpy')
                
                s = args[0]
                length = self.call(IntrinsicCallContext(pos, builder, module, 'string.length', [s]))
                ptr_copy = builder.call(malloc, [length], 'ptr_copy')
                is_null = self.call(IntrinsicCallContext(pos, builder, module, '==.pointer.pointer', [ptr_copy, NULL()]))
                with builder.if_then(is_null):
                    oom_text = 'out of memory'
                    oom_global = module.global_string(oom_text, 'oom_global')
                    oom_ptr = builder.first_elem(oom_global, 'oom_ptr')
                    oom_string = builder.struct(string_type, [oom_ptr, llint(len(oom_text))], 'oom_string')
                    ctx = IntrinsicCallContext(pos, builder, module, 'error', [oom_string])
                    self.call(ctx)

                ctx = IntrinsicCallContext(pos, builder, module, 'string.ptr', [s])
                ptr = self.call(ctx)
                builder.call(memcpy, [ptr_copy, ptr, length, llint(0, 1)])
                return builder.struct(string_type, [ptr_copy, length, llint(1, 1)], 'string.to_string')
            case _:
                raise NotImplementedError(name)
