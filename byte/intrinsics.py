from logging import info
from typing import Any

from llvmlite import ir

from byte.llvm_extensions import llint, NULL, IRBuilderExt, ModuleExt, Registry
from byte import ast


class Intrinsics:
    def __init__(self, file: ast.File):
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
        
        self.declare_empty_function('print', params=[ast.Param(ast.Position(), string_type, 's')])
        self.declare_empty_function('print_literal', params=[ast.Param(ast.Position(), string_type, 's')])
        self.declare_empty_function('string_struct', string_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), int_type, 'length'),
            ast.Param(ast.Position(), bool_type, 'is_allocated')
        ])
        
        self.declare_empty_function('gep', pointer_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'),
            ast.Param(ast.Position(), int_type, 'offset')
        ])
        
        self.declare_empty_function('store', params=[
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), any_type, 'value')
        ])
        
        self.declare_empty_function('input', string_type)
        self.declare_empty_function('error', params=[ast.Param(ast.Position(), string_type, 'message')])
        self.declare_empty_function('is_null', bool_type, [ast.Param(ast.Position(), pointer_type, 'ptr')])
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
    
    def declare_op_function(self, op: str, ret_type: ast.Type, a_type: ast.Type, b_type: ast.Type | None = None):
        if b_type is None:
            name = f'{op}.{a_type}'
            params = [ast.Param(ast.Position(), a_type, 'a')]
        else:
            name = f'{op}.{a_type}.{b_type}'
            params = [ast.Param(ast.Position(), a_type, 'a'), ast.Param(ast.Position(), b_type, 'b')]
        
        self.declare_empty_function(name, ret_type, params)
    
    def declare_attribute_function(self, object_type: ast.Type, attr_name: str,
        ret_type: ast.Type | None = None, params: list[ast.Param] | None = None,
        is_static: bool = False, is_method: bool = True):
        if params is None:
            params = []
        
        if not is_static:
            params.insert(0, ast.Param(ast.Position(), object_type, 'self'))
        
        flags = ast.FunctionFlags(static=is_static, property=not is_method, method=is_method)
        self.declare_empty_function(f'{object_type}.{attr_name}', ret_type, params, flags)
    
    def declare_empty_function(self, name: str, ret_type: ast.Type | None = None, params: list[ast.Param] | None = None,
        flags: ast.FunctionFlags | None = None):
        if flags is None:
            flags = ast.FunctionFlags()
        
        if params is None:
            params = []
        
        if ret_type is None:
            ret_type = self.file.type_map.get('nil')
        
        func = ast.Function(ast.Position(), ret_type, name, params, flags=flags)
        self.file.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
    
    def call(self, builder: IRBuilderExt, module: ModuleExt, name: str, args: list[Any]):
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
            case 'input':
                acrt_iob_func = module.registry.get('acrt_iob_func')
                strcspn = module.registry.get('strcspn')
                fgets = module.registry.get('fgets')
                
                BUF_SIZE = 512
                buf = module.try_get_global(
                    'input_buf', lambda: module.global_buffer(ir.IntType(8), BUF_SIZE, 'input_buf')
                )
                
                buf_ptr = builder.first_elem(buf, 'buf_ptr')
                stdin = builder.call(acrt_iob_func, [llint(0)], 'stdin')
                fgets_result = builder.call(fgets, [buf_ptr, llint(BUF_SIZE), stdin], 'fgets')
                fgets_failed = builder.icmp_signed('==', fgets_result, NULL(), 'fgets_failed')
                with builder.if_then(fgets_failed):
                    ERR_MSG = 'out of memory'
                    oom_length = llint(len(ERR_MSG))
                    oom_msg = module.try_get_global(
                        'out_of_memory_msg', lambda: module.global_string(ERR_MSG, 'out_of_memory_msg')
                    )
                    oom_msg_ptr = builder.first_elem(oom_msg, 'out_of_memory_msg_ptr')
                    
                    oom_str = builder.struct(string_type, [oom_msg_ptr, oom_length, llint(0, 1)], 'out_of_memory_str')
                    self.call(builder, module, 'error', [oom_str])
                
                newline_char = module.try_get_global('newline_char', lambda: module.global_string('\n', 'newline_char'))
                newline_char_ptr = builder.first_elem(newline_char, 'newline_char_ptr')
                newline_position = builder.call(strcspn, [buf_ptr, newline_char_ptr], 'newline_position')
                return builder.struct(string_type, [buf_ptr, newline_position, llint(0, 1)], 'string')
            case 'store':
                builder.store(args[1], args[0])
            case 'error':
                exit = module.registry.get('exit')
                
                self.call(builder, module, 'print', args)
                builder.call(exit, [llint(1)])
                # TODO: builder.unreachable()
            case 'is_null':
                return builder.icmp_signed('==', args[0], NULL(), 'is_null')
            case '+.pointer.int':
                return builder.gep(args[0], [args[1]], True, '+.pointer.int')
            case 'string.is_allocated':
                return builder.extract_value(args[0], 2, 'string.is_allocated')
            case 'null':
                return NULL()
