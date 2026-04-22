from logging import info
from typing import Any

from llvmlite import ir

from byte.llvm_extensions import llint, NULL, IRBuilderExt, ModuleExt, Registry
from byte import ast


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
        any_type = self.file.type_map.get('any')
        
        self.declare_op_function('+', int_type, int_type, int_type)
        self.declare_op_function('-', int_type, int_type, int_type)
        self.declare_op_function('*', int_type, int_type, int_type)
        self.declare_op_function('/', int_type, int_type, int_type)
        self.declare_op_function('%', int_type, int_type, int_type)
        self.declare_op_function('==', bool_type, int_type, int_type)
        self.declare_op_function('!=', bool_type, int_type, int_type)
        self.declare_op_function('>', bool_type, int_type, int_type)
        self.declare_op_function('<', bool_type, int_type, int_type)
        self.declare_op_function('>=', bool_type, int_type, int_type)
        self.declare_op_function('<=', bool_type, int_type, int_type)
        
        self.declare_op_function('+', float_type, float_type, float_type)
        self.declare_op_function('-', float_type, float_type, float_type)
        self.declare_op_function('*', float_type, float_type, float_type)
        self.declare_op_function('/', float_type, float_type, float_type)
        self.declare_op_function('%', float_type, float_type, float_type)
        self.declare_op_function('==', bool_type, float_type, float_type)
        self.declare_op_function('!=', bool_type, float_type, float_type)
        self.declare_op_function('>', bool_type, float_type, float_type)
        self.declare_op_function('<', bool_type, float_type, float_type)
        self.declare_op_function('>=', bool_type, float_type, float_type)
        self.declare_op_function('<=', bool_type, float_type, float_type)
        
        self.declare_op_function('==', bool_type, bool_type, bool_type)
        self.declare_op_function('!=', bool_type, bool_type, bool_type)
        self.declare_op_function('&&', bool_type, bool_type, bool_type)
        self.declare_op_function('||', bool_type, bool_type, bool_type)
        self.declare_op_function('!', bool_type, bool_type)
        
        self.declare_op_function('+', pointer_type, pointer_type, int_type)
        self.declare_op_function('==', bool_type, pointer_type, pointer_type)
        self.declare_op_function('!=', bool_type, pointer_type, pointer_type)
        
        self.declare_empty_function('print', params=[ast.Param(ast.Position(), string_type, 's')], public=True)
        self.declare_empty_function('print_literal', params=[ast.Param(ast.Position(), string_type, 's')], public=True)
        self.declare_empty_function('string_struct', string_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), int_type, 'length'),
            ast.Param(ast.Position(), bool_type, 'is_allocated')
        ])
        
        self.declare_empty_function('buffer', pointer_type, [ast.Param(ast.Position(), int_type, 'size')])
        self.declare_empty_function('gep', pointer_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'),
            ast.Param(ast.Position(), int_type, 'offset')
        ])
        
        self.declare_empty_function('store', params=[
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), any_type, 'value')
        ])
        
        self.declare_empty_function('error', params=[ast.Param(ast.Position(), string_type, 'message')], public=True)
        self.declare_empty_function('null', pointer_type)
        
        self.declare_attribute_function(int_type, 'to_string', string_type)
        self.declare_attribute_function(float_type, 'to_string', string_type)
        self.declare_attribute_function(string_type, 'to_string', string_type)
        self.declare_attribute_function(bool_type, 'to_string', string_type)
        
        self.declare_attribute_function(string_type, 'ptr', pointer_type, is_method=False)
        self.declare_attribute_function(string_type, 'length', int_type, is_method=False)
        self.declare_attribute_function(string_type, 'is_allocated', bool_type, is_method=False)
        
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
    
    def call(self, pos: ast.Position, builder: IRBuilderExt, module: ModuleExt, name: str, args: list[Any]):
        string_type = module.context.get_identified_type('string')
        
        info(f'calling intrinsic function {name} with {len(args)} arguments')
        match name:
            case '+.int.int':
                return builder.add(args[0], args[1], '+.int.int')
            case '-.int.int':
                return builder.sub(args[0], args[1], '-.int.int')
            case '*.int.int':
                return builder.mul(args[0], args[1], '*.int.int')
            case '/.int.int':
                return builder.sdiv(args[0], args[1], '/.int.int')
            case '%.int.int':
                return builder.srem(args[0], args[1], '%.int.int')
            case '==.int.int':
                return builder.icmp_signed('==', args[0], args[1], '==.int.int')
            case '!=.int.int':
                return builder.icmp_signed('!=', args[0], args[1], '!=.int.int')
            case '>.int.int':
                return builder.icmp_signed('>', args[0], args[1], '>.int.int')
            case '<.int.int':
                return builder.icmp_signed('<', args[0], args[1], '<.int.int')
            case '>=.int.int':
                return builder.icmp_signed('>=', args[0], args[1], '>=.int.int')
            case '<=.int.int':
                return builder.icmp_signed('<=', args[0], args[1], '<=.int.int')
            case '+.float.float':
                return builder.fadd(args[0], args[1], '+.float.float')
            case '-.float.float':
                return builder.fsub(args[0], args[1], '-.float.float')
            case '*.float.float':
                return builder.fmul(args[0], args[1], '*.float.float')
            case '/.float.float':
                return builder.fdiv(args[0], args[1], '/.float.float')
            case '%.float.float':
                return builder.frem(args[0], args[1], '%.float.float')
            case '==.float.float':
                return builder.fcmp_ordered('==', args[0], args[1], '==.float.float')
            case '!=.float.float':
                return builder.fcmp_ordered('!=', args[0], args[1], '!=.float.float')
            case '>.float.float':
                return builder.fcmp_ordered('>', args[0], args[1], '>.float.float')
            case '<.float.float':
                return builder.fcmp_ordered('<', args[0], args[1], '<.float.float')
            case '>=.float.float':
                return builder.fcmp_ordered('>=', args[0], args[1], '>=.float.float')
            case '<=.float.float':
                return builder.fcmp_ordered('<=', args[0], args[1], '<=.float.float')
            case '==.bool.bool':
                return builder.icmp_signed('==', args[0], args[1], '==.bool.bool')
            case '!=.bool.bool':
                return builder.icmp_signed('!=', args[0], args[1], '!=.bool.bool')
            case '&&.bool.bool':
                return builder.and_(args[0], args[1], '&&.bool.bool')
            case '||.bool.bool':
                return builder.or_(args[0], args[1], '||.bool.bool')
            case '!.bool':
                return builder.not_(args[0], '!.bool')
            case 'print':
                printf = module.registry.get('printf')
                fmt = module.try_get_global('string_fmt', lambda: module.global_string('%.*s\n', 'string_fmt'))
                ptr = builder.first_elem(fmt, 'string_fmt_ptr')
                s_ptr = builder.extract_value(args[0], 0, 's_ptr')
                s_length = builder.extract_value(args[0], 1, 's_length')
                builder.call(printf, [ptr, s_length, s_ptr])
            case 'print_literal':
                printf = module.registry.get('printf')
                fmt = module.try_get_global('string_lit_fmt', lambda: module.global_string('%.*s', 'string_lit_fmt'))
                ptr = builder.first_elem(fmt, 'string_lit_fmt_ptr')
                s_ptr = builder.extract_value(args[0], 0, 's_ptr')
                s_length = builder.extract_value(args[0], 1, 's_length')
                builder.call(printf, [ptr, s_length, s_ptr])
            case 'string_struct':
                return builder.struct(string_type, args, 'string_struct')
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
                return args[0]
            case 'bool.to_string':
                true_str = module.global_string('true', module.get_unique_name('true_str'))
                false_str = module.global_string('false', module.get_unique_name('false_str'))
                true_ptr = builder.first_elem(true_str, 'true_ptr')
                false_ptr = builder.first_elem(false_str, 'false_ptr')
                
                ptr = builder.select(args[0], true_ptr, false_ptr, 'b_ptr')
                length = builder.select(args[0], llint(4), llint(5), 'b_length')
                return builder.struct(string_type, [ptr, length, llint(0, 1)], 'bool.to_string')
            case 'gep':
                return builder.gep(args[0], [args[1]], True, 'gep')
            case 'string.length':
                return builder.extract_value(args[0], 1, 'string.length')
            case 'store':
                builder.store(args[1], args[0])
            case 'error':
                acrt_iob_func = module.registry.get('acrt_iob_func')
                fprintf = module.registry.get('fprintf')
                exit = module.registry.get('exit')
                
                stderr = builder.call(acrt_iob_func, [llint(2)], 'stderr')
                fmt = module.try_get_global('error_fmt', lambda: module.global_string('error: %.*s\n', 'error_fmt'))
                ptr = builder.first_elem(fmt, 'error_fmt_ptr')
                s_ptr = builder.extract_value(args[0], 0, 's_ptr')
                s_length = builder.extract_value(args[0], 1, 's_length')
                builder.call(fprintf, [stderr, ptr, s_length, s_ptr])
                builder.call(exit, [llint(1)])
                builder.unreachable()
            case '+.pointer.int':
                a, b = args
                return builder.gep(a, [b], True, '+.pointer.int')
            case 'string.is_allocated':
                return builder.extract_value(args[0], 2, 'string.is_allocated')
            case 'null':
                return NULL()
            case '==.pointer.pointer':
                a, b = args
                return builder.icmp_signed('==', a, b, '==.pointer.pointer')
            case '!=.pointer.pointer':
                a, b = args
                return builder.icmp_signed('!=', a, b, '!=.pointer.pointer')
            case 'buffer':
                if not isinstance(args[0], ir.Constant):
                    pos.comptime_error(self.file, 'expected literal integer')
                
                buf = module.global_buffer(ir.IntType(8), args[0].constant, module.get_unique_name('buffer'))
                return builder.first_elem(buf, f'{buf.name}.ptr')
