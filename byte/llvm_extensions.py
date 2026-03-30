from typing import Any, Callable, cast

from llvmlite import ir, binding


def llint(value: int, width: int = 32):
    """Returns an integer constant with the given width and value"""
    return ir.Constant(ir.IntType(width), value)

# TODO: support external variable definitions as well as external functions
class RegistryDefinition:
    def __init__(self, llvm_name: str, type: ir.FunctionType, display_name: str | None = None):
        self.llvm_name = llvm_name
        self.type = type
        self.display_name = display_name

class Registry:
    def __init__(self, module: ir.Module) -> None:
        self.module = module
        
        self.functions = {}
        self.globals = {}
        
        for definition in self.get_all_definitions():
            self.add_function(definition.llvm_name, definition.type, definition.display_name)
    
    @staticmethod
    def get_all_definitions():
        return [
            RegistryDefinition('printf', ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))], True)),
            RegistryDefinition('malloc', ir.FunctionType(ir.PointerType(ir.IntType(8)), [ir.IntType(32)])),
            RegistryDefinition('free', ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])),
            RegistryDefinition('llvm.memcpy.p0.p0.i32', ir.FunctionType(ir.VoidType(), [
                ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8)), ir.IntType(32)
            ]), 'memcpy'),
            
            RegistryDefinition('memcmp', ir.FunctionType(ir.IntType(1), [
                ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8)), ir.IntType(32)
            ])),
            
            RegistryDefinition('asprintf', ir.FunctionType(ir.IntType(32), [
                ir.PointerType(ir.PointerType(ir.IntType(8))), ir.PointerType(ir.IntType(8))
            ], True)),
            
            RegistryDefinition('llvm.sqrt.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'sqrt'),
            RegistryDefinition('llvm.pow.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]), 'pow'),
            RegistryDefinition('llvm.fabs.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'fabs'),
            RegistryDefinition('llvm.floor.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'floor'),
            RegistryDefinition('llvm.ceil.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'ceil'),
            RegistryDefinition('llvm.maxnum.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]), 'maxnum'),
            RegistryDefinition('llvm.minnum.f32', ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]), 'minnum'),
            RegistryDefinition('llvm.smax.i32', ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)]), 'smax'),
            RegistryDefinition('llvm.smin.i32', ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)]), 'smin')
        ]
    
    def add_function(self, name: str, func_type: ir.FunctionType, display_name: str | None = None):
        self.functions[display_name or name] = (name, func_type)
    
    def add_global(self, name: str, type: ir.Type, display_name: str | None = None):
        self.globals[display_name or name] = (name, type)
    
    def get(self, name: str):
        if name in self.functions:
            llvm_name, func_type = self.functions[name]
            if llvm_name in self.module.globals:
                return self.module.get_global(llvm_name)
            
            func = ir.Function(self.module, func_type, llvm_name)
            func.linkage = 'external'
            return func
        elif name in self.globals:
            llvm_name, type = self.globals[name]
            if llvm_name in self.module.globals:
                return self.module.get_global(llvm_name)
            
            return ir.GlobalVariable(self.module, type, llvm_name)
        
        raise NotImplementedError(name)

class ModuleExt(ir.Module):
    """An extension of `llvmlite.ir.Module`."""
    
    def __init__(self, name='', context=ir.context.global_context):
        super().__init__(name, context)
        
        self.registry = Registry(self)
        self.data = binding.create_target_data(self.data_layout)
    
    def declare_identified_type(self, name: str, *elem_types: ir.Type, packed: bool = False):
        """Adds a new identified type with the given name"""
        
        typ = self.context.get_identified_type(name, packed)
        if typ.is_opaque:
            typ.set_body(*elem_types)
        
        return typ
    
    def try_get_global(self, name: str, initialiser_fn: Callable[[], Any]):
        """Tries to get the global with the given name and initialising it using the given function if it does not exist"""
        
        if name in self.globals:
            return self.get_global(name)
        else:
            return initialiser_fn()
    
    def sizeof(self, type: ir.Type, width: int = 32):
        """Get the size of a type at compile-time in bytes with the given integer width"""
    
        return ir.Constant(ir.IntType(width), type.get_abi_size(self.data, self.context))
    
    def global_buffer(self, element_type: ir.Type, size: int, name = ''):
        """Create a global buffer variable\n
To get a pointer to the string, use `ir.Constant.gep`"""
        
        buf_type = ir.ArrayType(element_type, size)
        buf = ir.GlobalVariable(self, buf_type, name or self.get_unique_name('buf'))
        buf.initializer = cast(None, ir.Constant(buf_type, None))
        buf.linkage = 'internal'
        
        return buf
    
    def global_string(self, text: str, name: str = ''):
        """Creates a global string variable and returns it\n
To get a pointer to the string, use `ir.Constant.gep`"""
        
        text += '\0'
        const_type = ir.ArrayType(ir.IntType(8), len(text))
        const = ir.GlobalVariable(self, const_type, name or self.get_unique_name('str'))
        const.initializer = cast(None, ir.Constant(const_type, bytearray(text.encode())))
        const.global_constant = True
        const.linkage = 'internal'
        
        return const

class IRBuilderExt(ir.IRBuilder):
    """An extension of `llvmlite.ir.IRBuilder`."""
    
    def cast(self, value: Any, type: ir.Type, name: str = '') -> Any:
        """Converts the value to the type in any possible way"""
        
        value_type = value.type
        if isinstance(type, ir.IntType) and isinstance(value_type, ir.IntType):
            if type.width > value_type.width:
                return self.sext(value, type, name)
            elif type.width < value_type.width:
                return self.trunc(value, type, name)
            else:
                # type.width == value_type.width
                return value
        elif isinstance(type, ir.FloatType) and isinstance(value_type, ir.IntType):
            return self.sitofp(value, type, name)
        elif isinstance(type, ir.IntType) and isinstance(value_type, ir.FloatType):
            return self.fptosi(value, type, name)
        elif isinstance(type, ir.DoubleType) and isinstance(value_type, ir.FloatType):
            return self.fpext(value, type, name)
        elif isinstance(type, ir.FloatType) and isinstance(value_type, ir.DoubleType):
            return self.fptrunc(value, type, name)
        elif isinstance(type, ir.IntType) and isinstance(value_type, ir.PointerType):
            return self.ptrtoint(value, type, name)
        elif isinstance(type, ir.PointerType) and isinstance(value_type, ir.IntType):
            return self.inttoptr(value, type, name)
        elif isinstance(type, ir.PointerType) and isinstance(value_type, ir.PointerType):
            return self.bitcast(value, type, name)
        
        raise NotImplementedError(f'{value_type} -> {type}')
    
    def allocate_value(self, value: Any, name: str = ''):
        """Allocates a value on the stack and returns the pointer to it"""
        
        ptr = self.alloca(value.type, name=name)
        self.store(value, ptr)
        
        return ptr
    
    def struct(self, type: ir.Type, args: list[Any], name: str = ''):
        """Creates a new struct with the given type and arguments"""
        
        struct = ir.Constant(type, ir.Undefined)
        for i, arg in enumerate(args):
            struct = self.insert_value(struct, arg, i, name)
        
        return struct
    
    def first_elem(self, ptr: Any, name: str = '', inbounds: bool = True):
        """Gets the first element of a pointer or array"""
        
        return self.gep(ptr, [llint(0), llint(0)], inbounds, name)
    
    def null_terminate(self, ptr: Any, length: Any, name: str = '', ptr_width: int = 8, inbounds: bool = True):
        """Null terminates (adds \\0 at length in the given pointer) the pointer assuming that it is a pointer of 8 bit ints"""
        
        length_ptr = self.gep(ptr, [length], inbounds, name)
        self.store(llint(0, ptr_width), length_ptr)
