from typing import cast, Any
from logging import info

from llvmlite import ir, binding

from byte.llvm_extensions import ModuleExt, IRBuilderExt, llint
from byte.passes import ByteCompilerPass
from byte import ast


class CodeGeneration(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)
        
        self.module = ModuleExt(file.path.stem)
        self.module.triple = binding.get_default_triple()
        
        self.builder = IRBuilderExt()
        
        self.string_type = self.module.declare_identified_type('string', ir.PointerType(ir.IntType(8)), ir.IntType(32))
        
        self.define_c_registry()
        info('successfully created builder and module')
    
    def define_c_registry(self):
        self.module.registry.add_function('printf', ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))], True))
        self.module.registry.add_function('malloc', ir.FunctionType(ir.PointerType(ir.IntType(8)), [ir.IntType(32)]))
        self.module.registry.add_function('free', ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))]))
        self.module.registry.add_function('memcpy', ir.FunctionType(ir.VoidType(), [
            ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8)), ir.IntType(32)
        ]))
        
        self.module.registry.add_function('snprintf', ir.FunctionType(ir.IntType(32), [
            ir.PointerType(ir.IntType(8)), ir.IntType(32), ir.PointerType(ir.IntType(8))
        ], True))
        
        info('successfully registered external C functions')
    
    def visitProgram(self, node: ast.Program):
        for stmt in node.nodes:
            self.visit(stmt)
        
        return str(self.module)
    
    def visitType(self, node: ast.Type):
        match node.type:
            case 'int':
                return ir.IntType(32)
            case 'float':
                return ir.FloatType()
            case 'string':
                return self.string_type
            case 'bool':
                return ir.IntType(1)
            case 'nil':
                return ir.VoidType()
            case 'any' | 'pointer' | 'function':
                return ir.PointerType(ir.IntType(8))
    
    def visitArg(self, node: ast.Arg):
        return self.visit(node.value)
    
    def visitFunction(self, node: ast.Function):
        info(f'generating IR for function {node.name}')
        
        param_types = [self.visit(param.type) for param in node.params]
        ret_type = self.visit(node.ret_type)
        func = ir.Function(self.module, ir.FunctionType(ret_type, param_types), node.name)
        for arg, param in zip(func.args, node.params):
            arg.name = f'param.{param.name}'
        
        info(f'created IR function {node.name}')
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
        if node.body is not None:
            info(f'generating body for IR function {node.name}')
            with self.file.child_scope():
                old_builder = self.builder
                if len(node.params) > 0:
                    info('creating parameter allocation block')
                    param_allocation = func.append_basic_block('param_allocation')
                    self.builder.position_at_end(param_allocation)
                    for i, param in enumerate(node.params):
                        info(f'allocating {param.name}')
                        ptr = self.builder.allocate_value(func.args[i], f'{param.name}.addr')
                        self.scope.symbol_table.add(ast.Symbol(param.name, param.type, ptr, param.is_mutable))
                
                info('creating main entry block')
                entry_block = func.append_basic_block('entry')
                if len(node.params) > 0:
                    self.builder.branch(entry_block)
                    info('branching parameter allocation to entry block')
                
                self.builder.position_at_end(entry_block)
                self.visit(node.body)
                
                if not cast(ir.Block, self.builder.block).is_terminated:
                    self.builder.ret_void()
                    info('block is not terminated, returning void as a fallback')
                
                self.builder = old_builder
        
        return func
    
    def visitBody(self, node: ast.Body):
        for stmt in node.nodes:
            self.visit(stmt)
    
    def visitReturn(self, node: ast.Return):
        value = self.visit(node.value)
        self.builder.ret(value)
    
    def visitBreak(self, _):
        if (block := self.scope.data.codegen_while_merge_block) is not None:
            self.builder.branch(block)
    
    def visitContinue(self, _):
        if (block := self.scope.data.codegen_while_test_block) is not None:
            self.builder.branch(block)
    
    def visitIf(self, node: ast.If):
        func = cast(ir.Function, self.builder.function)
        merge_block = func.append_basic_block('if_merge')
        then_block = func.append_basic_block('if_then')

        elif_test_blocks = []
        elif_then_blocks = []

        for i in range(len(node.elseifs)):
            elif_test_blocks.append(func.append_basic_block(f'elif_test_{i}'))
            elif_then_blocks.append(func.append_basic_block(f'elif_then_{i}'))

        else_block = func.append_basic_block('if_else') if node.else_body is not None else merge_block

        cond = self.visit(node.cond)
        first_elif_test = elif_test_blocks[0] if elif_test_blocks else else_block
        self.builder.cbranch(cond, then_block, first_elif_test)

        self.builder.position_at_end(then_block)
        then_value = self.visit(node.body)
        if not cast(ir.Block, self.builder.block).is_terminated:
            self.builder.branch(merge_block)

        elif_end_blocks = []
        elif_values = []
        for i, elif_node in enumerate(node.elseifs):
            self.builder.position_at_end(elif_test_blocks[i])
            elif_cond = self.visit(elif_node.cond)

            next_target = elif_test_blocks[i + 1] if i + 1 < len(elif_test_blocks) else else_block
            self.builder.cbranch(elif_cond, elif_then_blocks[i], next_target)

            self.builder.position_at_end(elif_then_blocks[i])
            elif_value = self.visit(elif_node.body)
            if not cast(ir.Block, self.builder.block).is_terminated:
                self.builder.branch(merge_block)

            elif_end_blocks.append(self.builder.block)
            elif_values.append(elif_value)
        
        if else_block is not merge_block:
            self.builder.position_at_end(else_block)
            else_value = self.visit(cast(ast.Node, node.else_body))
            if not cast(ir.Block, self.builder.block).is_terminated:
                self.builder.branch(merge_block)

            else_end_block = self.builder.block
        else:
            else_value = None
            else_end_block = None

        self.builder.position_at_end(merge_block)

        all_values = [then_value] + elif_values + ([else_value] if else_value is not None else [])
        all_blocks = [then_block] + elif_end_blocks + ([else_end_block] if else_end_block is not None else [])

        if all(v is not None for v in all_values):
            phi = self.builder.phi(all_values[0].type)
            for val, blk in zip(all_values, all_blocks):
                phi.add_incoming(val, blk)

            return phi
    
    def visitWhile(self, node: ast.While):
        func = cast(ir.Function, self.builder.function)

        cond_block = func.append_basic_block('while_cond')
        body_block = func.append_basic_block('while_body')
        merge_block = func.append_basic_block('while_merge')

        self.builder.branch(cond_block)

        self.builder.position_at_end(cond_block)
        cond = self.visit(node.cond)
        self.builder.cbranch(cond, body_block, merge_block)

        self.builder.position_at_end(body_block)
        self.scope.data.codegen_while_merge_block = merge_block
        self.scope.data.codegen_while_test_block = cond_block
        self.visit(node.body)
        if not cast(ir.Block, self.builder.block).is_terminated:
            self.builder.branch(cond_block)

        self.builder.position_at_end(merge_block)
    
    def visitUse(self, node: ast.Use):
        lib_name = node.path
        stdlib_path = ast.STDLIB_PATH / f'{lib_name}.byte'
        if not stdlib_path.exists():
            node.pos.comptime_error(self.file, f'unknown library \'{lib_name}\'')
        
        from byte import compile_to_obj
        
        file = ast.File(stdlib_path)
        obj_file = compile_to_obj(file)
        for symbol in file.scope.symbol_table.symbols.values():
            func = symbol.value
            if not isinstance(func, ir.Function):
                continue
            
            extern_func = ir.Function(self.module, func.function_type, func.name)
            extern_func.linkage = 'external'
            
            info(f'found external function {func.name}')
        
        self.scope.symbol_table.merge(file.scope.symbol_table)
        self.file.type_map.merge(file.type_map)
        self.file.dependencies.append(obj_file)
        info(f'new dependency object file {obj_file}')
        return node
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        ptr = self.builder.allocate_value(value, f'{node.name}.addr')
        self.scope.symbol_table.add(ast.Symbol(node.name, node.type, ptr, node.is_mutable))
        info(f'allocated variable {node.name}')
        return ptr
    
    def visitAssignment(self, node: ast.Assignment):
        value = self.visit(node.value)
        symbol = self.scope.symbol_table.get(node.name)
        ptr = cast(Any, symbol.value)
        self.builder.store(value, ptr)
    
    def visitInt(self, node: ast.Int):
        return llint(node.value)
    
    def visitFloat(self, node: ast.Float):
        return ir.Constant(ir.FloatType(), node.value)
    
    def visitString(self, node: ast.String):
        string = self.module.global_string(node.value)
        return self.builder.first_elem(string, f'{string.name}.ptr')
    
    def visitBool(self, node: ast.Bool):
        return ir.Constant(ir.IntType(1), int(node.value))
    
    def visitId(self, node: ast.Id):
        symbol = self.scope.symbol_table.get(node.name)
        ptr = cast(Any, symbol.value)
        return self.builder.load(ptr, node.name)
    
    def internal_call(self, name: str, args: list[Any]):
        info(f'calling intrinsic function {name} with {len(args)} arguments')
        match name:
            case '+.int.int':
                return self.builder.add(args[0], args[1], '+.int.int')
            case '-.int.int':
                return self.builder.sub(args[0], args[1], '-.int.int')
            case '*.int.int':
                return self.builder.mul(args[0], args[1], '*.int.int')
            case '/.int.int':
                return self.builder.sdiv(args[0], args[1], '/.int.int')
            case '%.int.int':
                return self.builder.srem(args[0], args[1], '%.int.int')
            case '==.int.int':
                return self.builder.icmp_signed('==', args[0], args[1], '==.int.int')
            case '!=.int.int':
                return self.builder.icmp_signed('!=', args[0], args[1], '!=.int.int')
            case '>.int.int':
                return self.builder.icmp_signed('>', args[0], args[1], '>.int.int')
            case '<.int.int':
                return self.builder.icmp_signed('<', args[0], args[1], '<.int.int')
            case '>=.int.int':
                return self.builder.icmp_signed('>=', args[0], args[1], '>=.int.int')
            case '<=.int.int':
                return self.builder.icmp_signed('<=', args[0], args[1], '<=.int.int')
            case '+.float.float':
                return self.builder.fadd(args[0], args[1], '+.float.float')
            case '-.float.float':
                return self.builder.fsub(args[0], args[1], '-.float.float')
            case '*.float.float':
                return self.builder.fmul(args[0], args[1], '*.float.float')
            case '/.float.float':
                return self.builder.fdiv(args[0], args[1], '/.float.float')
            case '%.float.float':
                return self.builder.frem(args[0], args[1], '%.float.float')
            case '==.float.float':
                return self.builder.fcmp_ordered('==', args[0], args[1], '==.float.float')
            case '!=.float.float':
                return self.builder.fcmp_ordered('!=', args[0], args[1], '!=.float.float')
            case '>.float.float':
                return self.builder.fcmp_ordered('>', args[0], args[1], '>.float.float')
            case '<.float.float':
                return self.builder.fcmp_ordered('<', args[0], args[1], '<.float.float')
            case '>=.float.float':
                return self.builder.fcmp_ordered('>=', args[0], args[1], '>=.float.float')
            case '<=.float.float':
                return self.builder.fcmp_ordered('<=', args[0], args[1], '<=.float.float')
            case '==.bool.bool':
                return self.builder.icmp_signed('==', args[0], args[1], '==.bool.bool')
            case '!=.bool.bool':
                return self.builder.icmp_signed('!=', args[0], args[1], '!=.bool.bool')
            case '&&.bool.bool':
                return self.builder.and_(args[0], args[1], '&&.bool.bool')
            case '||.bool.bool':
                return self.builder.or_(args[0], args[1], '||.bool.bool')
            case '!.bool':
                return self.builder.not_(args[0], '!.bool')
            case 'print_int':
                printf = self.module.registry.get('printf')
                fmt = self.module.try_get_global('int_fmt', lambda: self.module.global_string('%d\n', 'int_fmt'))
                ptr = self.builder.first_elem(fmt, 'int_fmt_ptr')
                self.builder.call(printf, [ptr, args[0]])
            case 'print_float':
                printf = self.module.registry.get('printf')
                fmt = self.module.try_get_global('float_fmt', lambda: self.module.global_string('%f\n', 'float_fmt'))
                ptr = self.builder.first_elem(fmt, 'float_fmt_ptr')
                f_double = self.builder.fpext(args[0], ir.DoubleType(), 'f_double')
                self.builder.call(printf, [ptr, f_double])
            case 'print_string':
                printf = self.module.registry.get('printf')
                fmt = self.module.try_get_global('string_fmt', lambda: self.module.global_string('%s\n', 'string_fmt'))
                ptr = self.builder.first_elem(fmt, 'string_fmt_ptr')
                s_ptr = self.builder.extract_value(args[0], 0, 's_ptr')
                self.builder.call(printf, [ptr, s_ptr])
            case 'print_bool':
                printf = self.module.registry.get('printf')
                fmt = self.module.try_get_global('string_fmt', lambda: self.module.global_string('%s\n', 'string_fmt'))
                ptr = self.builder.first_elem(fmt, 'string_fmt_ptr')
                
                true_str = self.module.try_get_global('true_str', lambda: self.module.global_string('true', 'true_str'))
                false_str = self.module.try_get_global('false_str', lambda: self.module.global_string('false', 'false_str'))
                true_ptr = self.builder.first_elem(true_str, 'true_ptr')
                false_ptr = self.builder.first_elem(false_str, 'false_ptr')
                
                b_ptr = self.builder.select(args[0], true_ptr, false_ptr, 'b_ptr')
                self.builder.call(printf, [ptr, b_ptr])
            case 'malloc':
                malloc = self.module.registry.get('malloc')
                return self.builder.call(malloc, args, 'malloc')
            case 'free':
                free = self.module.registry.get('free')
                return self.builder.call(free, args)
            case 'memcpy':
                memcpy = self.module.registry.get('memcpy')
                return self.builder.call(memcpy, args, 'memcpy')
            case 'string_struct':
                return self.builder.struct(self.string_type, args, 'string_struct')
            case 'null_terminate':
                return self.builder.null_terminate(args[0], args[1], 'null_terminate')
            case 'string.ptr':
                return self.builder.extract_value(args[0], 0, 'string.ptr')
            case 'int.to_string':
                snprintf = self.module.registry.get('snprintf')
                
                BUF_SIZE = 16
                int_buf = self.module.global_buffer(ir.IntType(8), BUF_SIZE, f'int_buf{self.module.get_unique_name()}')
                int_buf_ptr = self.builder.first_elem(int_buf, 'int_buf_ptr')
                
                int_fmt = self.module.try_get_global('int_fmt', lambda: self.module.global_string('%d', 'int_fmt'))
                int_fmt_ptr = self.builder.first_elem(int_fmt, 'int_fmt_ptr')
                
                written = self.builder.call(snprintf, [int_buf_ptr, llint(BUF_SIZE), int_fmt_ptr, args[0]], 'written')
                return self.builder.struct(self.string_type, [int_buf_ptr, written], 'int.to_string')
            case 'float.to_string':
                snprintf = self.module.registry.get('snprintf')
                
                BUF_SIZE = 64
                float_buf = self.module.global_buffer(ir.IntType(8), BUF_SIZE, f'float_buf{self.module.get_unique_name()}')
                float_buf_ptr = self.builder.first_elem(float_buf, 'float_buf_ptr')
                
                float_fmt = self.module.try_get_global('float_fmt', lambda: self.module.global_string('%f', 'float_fmt'))
                float_fmt_ptr = self.builder.first_elem(float_fmt, 'float_fmt_ptr')
                
                f_double = self.builder.fpext(args[0], ir.DoubleType(), 'f_double')
                written = self.builder.call(snprintf, [float_buf_ptr, llint(BUF_SIZE), float_fmt_ptr, f_double], 'written')
                return self.builder.struct(self.string_type, [float_buf_ptr, written], 'float.to_string')
            case 'string.to_string':
                return args[0]
            case 'bool.to_string':
                true_str = self.module.try_get_global('true_str', lambda: self.module.global_string('true', 'true_str'))
                false_str = self.module.try_get_global('false_str', lambda: self.module.global_string('false', 'false_str'))
                true_ptr = self.builder.first_elem(true_str, 'true_ptr')
                false_ptr = self.builder.first_elem(false_str, 'false_ptr')
                
                ptr = self.builder.select(args[0], true_ptr, false_ptr, 'b_ptr')
                length = self.builder.select(args[0], llint(4), llint(5))
                return self.builder.struct(self.string_type, [ptr, length], 'bool.to_string')
    
    def visitCall(self, node: ast.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        func = cast(ast.Function | ir.Function, symbol.value)
        args = [self.visit(arg) for arg in node.args]
        if isinstance(func, ast.Function) and func.body is None:
            return self.internal_call(node.callee, args)
        
        info(f'calling function {node.callee}')
        return self.builder.call(func, args, node.callee)
    
    def visitTernary(self, node: ast.Ternary):
        return self.builder.select(self.visit(node.cond), self.visit(node.true), self.visit(node.false), 'ternary')
    
    def visitBracketed(self, node: ast.Bracketed):
        return self.visit(node.value)
