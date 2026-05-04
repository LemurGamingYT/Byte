from typing import Any, Callable, cast, TypeAlias
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from logging import info
from math import pi, e

from llvmlite import ir

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
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')
        Math_type = self.file.type_map.get('Math')
        System_type = self.file.type_map.get('System')
        
        self.declare_attribute_function(int_type, 'min', int_type, is_static=True, is_method=False)
        self.declare_attribute_function(int_type, 'max', int_type, is_static=True, is_method=False)
        self.declare_attribute_function(int_type, 'to_string', string_type)
        
        # self.declare_attribute_function(float_type, 'min', float_type, is_static=True, is_method=False)
        # self.declare_attribute_function(float_type, 'max', float_type, is_static=True, is_method=False)
        self.declare_attribute_function(float_type, 'to_string', string_type)
        
        self.declare_attribute_function(string_type, 'to_string', string_type)
        self.declare_attribute_function(bool_type, 'to_string', string_type)
        
        self.declare_attribute_function(string_type, 'ptr', pointer_type, is_method=False)
        self.declare_attribute_function(string_type, 'length', int_type, is_method=False)
        self.declare_attribute_function(string_type, 'is_allocated', bool_type, is_method=False)
        
        self.declare_attribute_function(Math_type, 'pi', float_type, is_static=True, is_method=False)
        self.declare_attribute_function(Math_type, 'e', float_type, is_static=True, is_method=False)
        
        self.declare_attribute_function(System_type, 'os', string_type, is_static=True, is_method=False)
        self.declare_attribute_function(System_type, 'pid', int_type, is_static=True, is_method=False)
        self.declare_attribute_function(System_type, 'sleep', params=[
            ast.Param(ast.Position(), int_type, 'milliseconds')
        ], is_static=True)
        
        for definition in Registry.get_all_definitions():
            name = definition.display_name or definition.llvm_name
            param_types = [ast.Type.from_llvm(self.file, ir_type) for ir_type in definition.type.args]
            params = [ast.Param(ast.Position(), type, str(i)) for i, type in enumerate(param_types)]
            ret_type = ast.Type.from_llvm(self.file, definition.type.return_type)
            self.declare_empty_function(name, ret_type, params)
            info(f'declared C registry function {name}')
    
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
            case 'string.ptr':
                return builder.extract_value(args[0], 0, 'string.ptr')
            case 'int.to_string':
                snprintf = module.registry.get('snprintf')
                
                int_fmt = module.try_get_global('int_fmt', lambda: module.global_string('%d', 'int_fmt'))
                int_fmt_ptr = builder.first_elem(int_fmt, 'int_fmt_ptr')
                
                BUF_SIZE = 16
                int_buf = builder.first_elem(
                    module.global_buffer(ir.IntType(8), BUF_SIZE, module.get_unique_name('int_buf')),
                    'int_buf'
                )
                
                written = builder.call(snprintf, [int_buf, llint(BUF_SIZE), int_fmt_ptr, args[0]], 'written')
                # TODO: check if snprintf failed
                
                return builder.struct(string_type, [int_buf, written, llint(0, 1)], 'int.to_string')
            case 'float.to_string':
                snprintf = module.registry.get('snprintf')
                
                float_fmt = module.try_get_global('float_fmt', lambda: module.global_string('%f', 'float_fmt'))
                float_fmt_ptr = builder.first_elem(float_fmt, 'float_fmt_ptr')
                
                f_double = builder.fpext(args[0], ir.DoubleType(), 'f_double')
                
                BUF_SIZE = 64
                float_buf = builder.first_elem(
                    module.global_buffer(ir.IntType(8), BUF_SIZE, module.get_unique_name('float_buf')),
                    'float_buf'
                )
                
                written = builder.call(snprintf, [float_buf, llint(BUF_SIZE), float_fmt_ptr, f_double], 'written')
                return builder.struct(string_type, [float_buf, written, llint(0, 1)], 'float.to_string')
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
                return builder.struct(string_type, [ptr_copy, length, llint(0, 1)], 'string.to_string')
            case 'bool.to_string':
                true_str = module.global_string('true', module.get_unique_name('true_str'))
                false_str = module.global_string('false', module.get_unique_name('false_str'))
                true_ptr = builder.first_elem(true_str, 'true_ptr')
                false_ptr = builder.first_elem(false_str, 'false_ptr')
                
                ptr = builder.select(args[0], true_ptr, false_ptr, 'b_ptr')
                length = builder.select(args[0], llint(4), llint(5), 'b_length')
                return builder.struct(string_type, [ptr, length, llint(0, 1)], 'bool.to_string')
            case 'string.length':
                return builder.extract_value(args[0], 1, 'string.length')
            case 'string.is_allocated':
                return builder.extract_value(args[0], 2, 'string.is_allocated')
            case 'int.min':
                return llint(-2147483648)
            case 'int.max':
                return llint(2147483647)
            case 'float.min':
                return ir.Constant(ir.FloatType(), 1.175494e-38)
            case 'float.max':
                return ir.Constant(ir.FloatType(), 3.402823e+38)
            case 'System.os':
                text = self.file.target.name.title()
                os_name = module.global_string(text, 'os_name')
                os_name_ptr = builder.first_elem(os_name, 'os_name_ptr')
                return builder.struct(string_type, [os_name_ptr, llint(len(text)), llint(0, 1)], 'System.os')
            case 'System.sleep':
                duration = args[0]
                
                if self.file.target == ast.Target.WINDOWS:
                    Sleep = module.registry.get('Sleep')
                    builder.call(Sleep, [duration])
                else:
                    usleep = module.registry.get('usleep')
                    duration_microseconds = builder.mul(duration, llint(1000), 'duration_microseconds')
                    builder.call(usleep, [duration_microseconds])
            case 'System.pid':
                if self.file.target == ast.Target.WINDOWS:
                    GetCurrentProcessId = module.registry.get('GetCurrentProcessId')
                    return builder.call(GetCurrentProcessId, [], 'System.pid')
                else:
                    getpid = module.registry.get('getpid')
                    return builder.call(getpid, [], 'System.pid')
            case 'Math.pi':
                return ir.Constant(ir.FloatType(), pi)
            case 'Math.e':
                return ir.Constant(ir.FloatType(), e)
            case _:
                raise NotImplementedError(name)
