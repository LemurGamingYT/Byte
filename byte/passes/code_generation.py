from dataclasses import dataclass
from typing import cast, Any
from logging import info

from llvmlite import ir, binding

from byte.llvm_extensions import ModuleExt, IRBuilderExt, llint
from byte.intrinsics import Intrinsics, IntrinsicCallContext
from byte.passes import ByteCompilerPass
from byte import ast


@dataclass
class CompileResult:
    module: ModuleExt

class CodeGeneration(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)
        
        self.module = ModuleExt(file.path.stem)
        self.module.triple = binding.get_default_triple()
        
        self.builder = IRBuilderExt()
        
        self.intrinsics = Intrinsics(file)
        
        self.string_type = self.module.declare_identified_type(
            'string', ir.PointerType(ir.IntType(8)), ir.IntType(32), ir.IntType(1)
        )
        
        self.class_types = {}
        self.class_field_names = {}
        
        info('successfully created builder and module')
    
    def visitProgram(self, node: ast.Program):
        for stmt in node.nodes:
            self.visit(stmt)
        
        return CompileResult(self.module)
    
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
            case _:
                if node.type in self.class_types:
                    return self.class_types[node.type]
                
                raise NotImplementedError(node.type)
    
    def visitReferenceType(self, node: ast.ReferenceType):
        return ir.PointerType(self.visit(node.type))
    
    def visitArg(self, node: ast.Arg):
        return self.visit(node.value)
    
    def visitFunction(self, node: ast.Function):
        if node.is_generic:
            return node
        
        if node.name in self.module.globals:
            return self.module.get_global(node.name)
        
        info(f'generating IR for function {node.name}')
        
        is_generic_expansion = node.name.endswith('>')
        param_types = [self.visit(param.type) for param in node.params]
        ret_type = self.visit(node.ret_type)
        func = ir.Function(self.module, ir.FunctionType(ret_type, param_types), node.name)
        for arg, param in zip(func.args, node.params):
            arg.name = f'param.{param.name}'
        
        if is_generic_expansion:
            func.linkage = 'linkonce_odr dso_local'
        
        info(f'created IR function {node.name}')
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
        if node.body is not None:
            info(f'generating body for IR function {node.name}')
            with self.file.child_scope():
                old_builder = self.builder
                
                if len(node.params) > 0:
                    info('creating parameter allocation block')
                    param_allocation = func.append_basic_block('param_allocation')
                    self.builder = IRBuilderExt(param_allocation)
                    for i, param in enumerate(node.params):
                        info(f'allocating {param.name}')
                        ptr = self.builder.allocate_value(func.args[i], f'{param.name}.addr')
                        self.scope.symbol_table.add(ast.Symbol(param.name, param.type, ptr, param.is_mutable))
                
                info('creating main entry block')
                entry_block = func.append_basic_block('entry')
                if len(node.params) > 0:
                    self.builder.branch(entry_block)
                    info('branching parameter allocation to entry block')
                
                self.builder = IRBuilderExt(entry_block)
                self.visit(node.body)
                
                if not cast(ir.Block, self.builder.block).is_terminated:
                    if str(node.ret_type) == 'nil':
                        self.builder.ret_void()
                    else:
                        self.builder.unreachable()
                
                self.builder = old_builder
        
        return func
    
    def visitClass(self, node: ast.Class):
        info(f'generating IR for class {node.name}')
        fields = [member for member in node.members if isinstance(member, ast.Property)]
        field_types = [cast(ir.Type, self.visit(field.type)) for field in fields]
        cls_type = self.module.declare_identified_type(node.name, *field_types)
        self.class_types[node.name] = cls_type
        self.class_field_names[node.name] = [field.name for field in fields]
        
        for member in node.members:
            if isinstance(member, ast.Property):
                continue
            
            self.visit(member)
        
        return node
    
    def visitBody(self, node: ast.Body):
        for stmt in node.nodes:
            if cast(ir.Block, self.builder.block).is_terminated:
                break
            
            self.visit(stmt)
    
    def visitReturn(self, node: ast.Return):
        if node.value is None:
            return self.builder.ret_void()
        
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
        if lib_name == 'intrinsics':
            return node # already handled in type checker pass
        
        stdlib_path = ast.STDLIB_PATH / f'{lib_name}.byte'
        if not stdlib_path.exists():
            node.pos.comptime_error(self.file, f'unknown library \'{lib_name}\'')
        
        from byte import compile_to_obj
        
        file = ast.File(stdlib_path, options=self.file.options, target=self.file.target)
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
        if isinstance(symbol.type, ast.ReferenceType):
            ptr = self.builder.load(ptr, f'{symbol.name}.ref')
        
        self.builder.store(value, ptr)
    
    def visitForRange(self, node: ast.ForRange):
        func = cast(ir.Function, self.builder.function)
        
        cond_block = func.append_basic_block('for_range_cond')
        body_block = func.append_basic_block('for_range_body')
        inc_block = func.append_basic_block('for_inc_body')
        merge_block = func.append_basic_block('for_merge_block')
        
        self.scope.data.codegen_while_merge_block = merge_block
        self.scope.data.codegen_while_test_block = cond_block
        
        if node.step is None:
            raise RuntimeError('node.step still not evaluated')
        
        start = self.visit(node.start)
        end = self.visit(node.end)
        step = self.visit(node.step)
        is_decrementing = self.builder.icmp_signed('>', start, end, 'is_decrementing')
        with self.builder.if_then(is_decrementing):
            err_msg = 'for range loop start is greater than end'
            err_msg_global = self.module.global_string(err_msg, 'loop_error')
            err_msg_ptr = self.builder.first_elem(err_msg_global, 'err_msg_ptr')
            err_msg_string = self.builder.struct(self.string_type, [err_msg_ptr, llint(len(err_msg))], 'err_msg_string')

            ctx = IntrinsicCallContext(node.pos, self.builder, self.module, 'error', [err_msg_string])
            self.intrinsics.call(ctx)
        
        var_ptr = self.builder.allocate_value(start, name=f'{node.iter_name}.addr')
        self.builder.branch(cond_block)
        self.builder.position_at_end(cond_block)
        
        var_value = self.builder.load(var_ptr, node.iter_name)
        cond = self.builder.icmp_signed('<', var_value, end, 'cond')
        self.builder.cbranch(cond, body_block, merge_block)
        self.builder.position_at_end(body_block)
        
        self.scope.symbol_table.add(ast.Symbol(node.iter_name, node.start.type, var_ptr))
        self.visit(node.body)
        
        self.builder.branch(inc_block)
        self.builder.position_at_end(inc_block)
        
        var_value = self.builder.load(var_ptr, node.iter_name)
        if isinstance(start.type, ir.IntType):
            var_inc = self.builder.add(var_value, step, 'var_inc')
        else:
            var_inc = self.builder.fadd(var_value, step, 'var_inc')
        
        self.builder.store(var_inc, var_ptr)
        self.builder.branch(cond_block)
        self.builder.position_at_end(merge_block)
    
    def visitInt(self, node: ast.Int):
        return llint(node.value)
    
    def visitFloat(self, node: ast.Float):
        return ir.Constant(ir.FloatType(), node.value)
    
    def visitString(self, node: ast.String):
        string = self.module.global_string(node.value, self.module.get_unique_name('str'))
        return self.builder.first_elem(string, f'{string.name}.ptr')
    
    def visitStringPointer(self, node: ast.StringPointer):
        string = self.module.global_string(node.value, self.module.get_unique_name('str'))
        return self.builder.first_elem(string, f'{string.name}.ptr')
    
    def visitBool(self, node: ast.Bool):
        return ir.Constant(ir.IntType(1), int(node.value))
    
    def visitId(self, node: ast.Id):
        symbol = self.scope.symbol_table.get(node.name)
        ptr = cast(Any, symbol.value)
        if isinstance(symbol.type, ast.ReferenceType):
            ptr = self.builder.load(ptr, f'{node.name}.ref')
        
        return self.builder.load(ptr, node.name)
    
    def visitCall(self, node: ast.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        func = cast(ast.Function | ir.Function, symbol.value)
        args = [self.visit(arg) for arg in node.args]
        if isinstance(func, ast.Function):
            if node.callee in self.module.registry.functions:
                ir_func = self.module.registry.get(node.callee)
                return self.builder.call(ir_func, args, node.callee)
            
            if func.body is not None:
                func = self.visitFunction(func)
            else:
                ctx = IntrinsicCallContext(node.pos, self.builder, self.module, node.callee, args)
                return self.intrinsics.call(ctx)
        
        info(f'calling function {node.callee}')
        return self.builder.call(func, args, node.callee)
    
    def visitTernary(self, node: ast.Ternary):
        return self.builder.select(self.visit(node.cond), self.visit(node.true), self.visit(node.false), 'ternary')
    
    def visitBracketed(self, node: ast.Bracketed):
        return self.visit(node.value)
    
    def visitRef(self, node: ast.Ref):
        symbol = self.scope.symbol_table.get(node.name)
        return symbol.value
    
    def visitStructLiteral(self, node: ast.StructLiteral):
        struct_type = self.module.get_identified_types().get(node.name)
        assert struct_type is not None
        
        args = [self.visit(arg) for arg in node.args]
        return self.builder.struct(struct_type, args, node.name)
    
    def visitStructPropertyGetter(self, node: ast.StructPropertyGetter):
        struct = self.visit(node.struct)
        assert isinstance(struct, ir.LoadInstr)
        
        cls_type = struct.type
        assert isinstance(cls_type, ir.IdentifiedStructType)
        
        cls_name = cls_type.name
        field_order = self.class_field_names[cls_name]
        idx = field_order.index(node.property_name)
        return self.builder.extract_value(struct, idx, node.property_name)
