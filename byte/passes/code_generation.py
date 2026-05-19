from dataclasses import dataclass
from typing import cast, Any
from pathlib import Path
from logging import info

from llvmlite import ir, binding as llvm

from byte.llvm_extensions import ModuleExt, IRBuilderExt, llint
from byte.intrinsics import IntrinsicCallContext
from byte.passes import ByteCompilerPass
from byte import ast


@dataclass
class CompileResult:
    module: ModuleExt

class CodeGeneration(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)
        
        self.module = ModuleExt(file.path.stem, ir.Context())
        self.module.triple = llvm.get_default_triple()
        
        self.builder = IRBuilderExt()
        
        self.string_type = self.module.declare_identified_type(
            'string', ir.PointerType(ir.IntType(8)), ir.IntType(32), ir.IntType(1)
        )
        
        info('successfully created builder and module')

    def define_array_struct(self, node: ast.ArrayType):
        T = cast(ir.Type, self.visit(node.type))
        elements = [ir.PointerType(T), ir.IntType(32)] # TODO: convert to using ir.VectorType
        return self.module.declare_identified_type(str(node), *elements)
    
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
                raise NotImplementedError(node.type)
    
    def visitReferenceType(self, node: ast.ReferenceType):
        return ir.PointerType(self.visit(node.type))

    def visitClassType(self, node: ast.ClassType):
        elements = [cast(ir.Type, self.visit(field_type)) for field_type in node.fields]
        return self.module.declare_identified_type(node.name, *elements)

    def visitArrayType(self, node: ast.ArrayType):
        return self.define_array_struct(node)
    
    def visitArg(self, node: ast.Arg):
        if isinstance(node.value, ast.Node):
            return self.visit(node.value)

        return node.value
    
    def visitFunction(self, node: ast.Function):
        if node.is_generic or callable(node.body):
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
        
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
        if isinstance(node.body, ast.Body):
            with self.file.child_scope():
                old_builder = self.builder
                
                if len(node.params) > 0:
                    param_allocation = func.append_basic_block('param_allocation')
                    self.builder = IRBuilderExt(param_allocation)
                    for i, param in enumerate(node.params):
                        info(f'allocating {param.name}')
                        ptr = self.builder.allocate_value(func.args[i], f'{param.name}.addr')
                        self.scope.symbol_table.add(ast.Symbol(
                            param.name, param.type, ptr, ast.SymbolFlags(mutable=param.flags.mutable)
                        ))
                
                entry_block = func.append_basic_block('entry')
                if len(node.params) > 0:
                    self.builder.branch(entry_block)
                
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
        
        self.visit(self.file.type_map.get(node.name))
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

    def use_byte(self, file: ast.File, path: Path):
        from byte import Pipeline
        
        if file.path.stem == self.file.path.stem:
            return

        file.path = path
        pipeline = Pipeline()
        _, obj_file = pipeline.compile_to_obj(file)
        for symbol in file.scope.symbol_table.symbols.values():
            func = symbol.value
            if not isinstance(func, ir.Function) or func.name in self.module.globals:
                continue
            
            extern_func = ir.Function(self.module, func.function_type, func.name)
            extern_func.linkage = 'external'
            
            info(f'found external function {func.name}')
        
        self.scope.symbol_table.merge(file.scope.symbol_table)
        self.file.type_map.merge(file.type_map)
        self.file.dependencies.append(obj_file)
        info(f'new dependency object file {obj_file}')
    
    def visitUse(self, node: ast.Use):
        stdlib_path = ast.STDLIB_PATH / node.path
        file = ast.File(stdlib_path, options=self.file.options, target=self.file.target)
        if stdlib_path.is_dir():
            for byte_file in stdlib_path.rglob('*.byte'):
                self.use_byte(file, byte_file)
        else:
            byte_file = ast.STDLIB_PATH / f'{node.path}.byte'
            if byte_file.exists():
                self.use_byte(file, byte_file)
        
        return node
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        ptr = self.builder.allocate_value(value, f'{node.name}.addr')
        self.scope.symbol_table.add(ast.Symbol(node.name, node.type, ptr, ast.SymbolFlags(mutable=node.is_mutable)))
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
            err_msg_global = self.module.try_get_global('loop_error', lambda: self.module.global_string(err_msg, 'loop_error'))
            err_msg_ptr = self.builder.first_elem(err_msg_global, 'err_msg_ptr')
            err_msg_string = self.builder.struct(self.string_type, [err_msg_ptr, llint(len(err_msg))], 'err_msg_string')

            self.call(node.pos, 'error', [
                ast.Arg(node.pos, self.file.type_map.get('string'), err_msg_string)
            ])
        
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

    def fix_args(self, ir_func: ir.Function, args: list[Any]):
        for i, (arg, param) in enumerate(zip(args, getattr(ir_func, 'args'))):
            if isinstance(param.type, ir.IntType) and param.type.width == 8:
                args[i] = self.builder.trunc(arg, ir.IntType(8), 'trunc')

    def call(self, pos: ast.Position, name: str, args: list[ast.Arg]):
        symbol = self.scope.symbol_table.get(name)
        func = cast(ast.Function | ir.Function, symbol.value)
        ir_args = [self.visit(arg) for arg in args]
        if isinstance(func, ast.Function):
            if name in self.module.registry.functions:
                ir_func = cast(ir.Function, self.module.registry.get(name))
                self.fix_args(ir_func, ir_args)
                return self.builder.call(ir_func, ir_args, name)

            if isinstance(func.body, ast.Body):
                func = self.visitFunction(func)
            else:
                ctx = IntrinsicCallContext(pos, self.builder, self.module, self.file, name, self, args, ir_args)
                if callable(func.body):
                    return func.body(ctx)
                
                raise NotImplementedError
        
        info(f'calling function {name}')
        self.fix_args(cast(ir.Function, func), ir_args)
        return self.builder.call(func, ir_args, name)
    
    def visitCall(self, node: ast.Call):
        return self.call(node.pos, node.callee, node.args)

    def visitNewArray(self, node: ast.NewArray):
        self.define_array_struct(cast(ast.ArrayType, node.type))
        return self.call(node.pos, f'{node.type}.new', [])
    
    def visitTernary(self, node: ast.Ternary):
        return self.builder.select(self.visit(node.cond), self.visit(node.true), self.visit(node.false), 'ternary')
    
    def visitBracketed(self, node: ast.Bracketed):
        return self.visit(node.value)
    
    def visitRef(self, node: ast.Ref):
        symbol = self.scope.symbol_table.get(node.name)
        return symbol.value

    def visitDeref(self, node: ast.Deref):
        symbol = self.scope.symbol_table.get(node.name)
        ptr = cast(Any, symbol.value)
        return self.builder.load(ptr, node.name)
    
    def visitStructLiteral(self, node: ast.StructLiteral):
        struct_type = self.module.context.get_identified_type(node.name)
        assert struct_type is not None
        
        args = [self.visit(arg) for arg in node.args]
        return self.builder.struct(struct_type, args, node.name)
