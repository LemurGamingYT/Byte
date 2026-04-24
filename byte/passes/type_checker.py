from logging import info
from typing import cast

from byte.passes import ByteCompilerPass
from byte.intrinsics import Intrinsics
from byte import ast


def length_word(word: str, count: int):
    if count == 0:
        return f'no {word}s'
    elif count == 1:
        return f'{count} {word}'
    else:
        return f'{count} {word}s'

class TypeChecker(ByteCompilerPass):
    def visitType(self, node: ast.Type):
        typ = self.file.type_map.tryget(node.type)
        if typ is None:
            node.pos.comptime_error(self.file, f'unknown type \'{node.type}\'')
        
        return typ
    
    def visitArg(self, node: ast.Arg):
        value = self.visit(node.value)
        return ast.Arg(node.pos, value.type, value)
    
    def visitParam(self, node: ast.Param):
        return ast.Param(node.pos, cast(ast.Type, self.visit(node.type)), node.name, node.is_mutable)
    
    def visitBody(self, node: ast.Body):
        return ast.Body(node.pos, cast(ast.Type, self.visit(node.type)), [self.visit(stmt) for stmt in node.nodes])
    
    def visitBreak(self, node: ast.Break):
        if not self.scope.in_loop:
            node.pos.comptime_error(self.file, 'break statement used outside loop')
        
        return node
    
    def visitContinue(self, node: ast.Continue):
        if not self.scope.in_loop:
            node.pos.comptime_error(self.file, 'continue statement used outside loop')
        
        return node
    
    def visitReturn(self, node: ast.Return):
        if node.value is None:
            return node
        
        value = self.visit(node.value)
        return ast.Return(node.pos, value.type, value)
    
    def have_same_types(self, list1: list[ast.Type], list2: list[ast.Type]):
        if len(list1) != len(list2):
            return False
        
        return all(type1 == type2 for type1, type2 in zip(list1, list2))
    
    def visitFunction(self, node: ast.Function):
        params = [cast(ast.Param, self.visit(param)) for param in node.params]
        ret_type = cast(ast.Type, self.visit(node.ret_type))
        extend_type = cast(ast.Type, self.visit(node.extend_type)) if node.extend_type is not None else None
        name = node.name
        if name in ('+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&&', '||'):
            if len(params) != 2:
                node.pos.comptime_error(self.file, f'operator overload of \'{name}\' must have two parameters')
            
            a, b = params
            name = f'{name}.{a.type}.{b.type}'
        elif name == '!':
            if len(params) != 1:
                node.pos.comptime_error(self.file, f'operator overload of \'{name}\' must have one parameter')
            
            a = params[0]
            name = f'{name}.{a.type}'
        
        if extend_type is not None:
            name = f'{extend_type}.{name}'
        
        func = ast.Function(node.pos, ret_type, name, params, node.body, node.flags)
        if self.scope.symbol_table.has(func.name):
            symbol = self.scope.symbol_table.get(func.name)
            base = cast(ast.Function, symbol.value)
            base.overloads.append(func)
            info(f'adding new overload to {base.name}')
            
            base_param_types = [param.type for param in base.params]
            param_types = [param.type for param in params]
            if self.have_same_types(base_param_types, param_types):
                node.pos.comptime_error(self.file, f'an overload of {func.name} has the same types as this overload')
            
            params_mangling = '.'.join(map(str, param_types))
            mangled_name = f'{func.name}.{params_mangling}'
            info(f'mangled overload function name \'{func.name}\' to \'{mangled_name}\'')
            
            func.name = mangled_name
        
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
        if func.body is not None:
            with self.file.child_scope():
                for param in params:
                    self.scope.symbol_table.add(param.to_symbol())
                
                func.body = cast(ast.Body, self.visit(func.body))
        
        return func
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        if self.scope.symbol_table.has(node.name):
            return self.visit(ast.Assignment(node.pos, value.type, node.name, value, node.op))
        
        self.scope.symbol_table.add(ast.Symbol(node.name, value.type, value, node.is_mutable))
        return ast.Variable(node.pos, value.type, node.name, value, node.is_mutable)
    
    def visitAssignment(self, node: ast.Assignment):
        symbol = self.scope.symbol_table.get(node.name)
        if not symbol.is_mutable:
            node.pos.comptime_error(self.file, f'\'{node.name}\' is immutable')
        
        value = node.value
        if node.op is not None:
            value = self.visit(ast.Operation(
                node.value.pos, node.type, node.op, ast.Id(node.pos, node.type, node.name), node.value
            ))
        
        return ast.Assignment(node.pos, node.type, node.name, value)
    
    def visitElseif(self, node: ast.Elseif):
        with self.file.child_scope():
            body = cast(ast.Body, self.visit(node.body))
        
        return ast.Elseif(node.pos, self.visit(node.cond), body)
    
    def visitIf(self, node: ast.If):
        with self.file.child_scope():
            body = cast(ast.Body, self.visit(node.body))
        
        if node.else_body is not None:
            with self.file.child_scope():
                else_body = cast(ast.Body, self.visit(node.else_body))
        else:
            else_body = None
        
        return ast.If(node.pos, self.visit(node.cond), body, else_body, [
            cast(ast.Elseif, self.visit(elseif)) for elseif in node.elseifs
        ])
    
    def visitWhile(self, node: ast.While):
        with self.file.child_scope():
            self.scope.in_loop = True
            
            body = cast(ast.Body, self.visit(node.body))
        
        return ast.While(node.pos, self.visit(node.cond), body)
    
    def visitUse(self, node: ast.Use):
        lib_name = node.path
        if lib_name == 'intrinsics':
            intrinsics = Intrinsics(self.file)
            intrinsics.register()
            return node
        
        stdlib_path = ast.STDLIB_PATH / f'{lib_name}.byte'
        if not stdlib_path.exists():
            node.pos.comptime_error(self.file, f'unknown library \'{lib_name}\'')
        
        from byte import parse
        
        file = ast.File(stdlib_path)
        program = parse(file)
        program = TypeChecker.run(file, program)
        
        self.scope.symbol_table.merge(file.scope.symbol_table)
        self.file.type_map.merge(file.type_map)
        
        info(f'used library {node.path} at {stdlib_path}')
        return node
    
    def visitId(self, node: ast.Id):
        symbol = self.scope.symbol_table.tryget(node.name)
        typ = self.file.type_map.tryget(node.name)
        if symbol is None and typ is None:
            node.pos.comptime_error(self.file, f'unknown identifier \'{node.name}\'')
        
        return ast.Id(node.pos, symbol.type if symbol is not None else cast(ast.Type, typ), node.name)
    
    def check_args(self, args: list[ast.Arg], params: list[ast.Param]):
        if len(args) != len(params):
            return False
        
        for arg, param in zip(args, params):
            arg_type = arg.type
            param_type = param.type
            if arg_type == param_type or str(param_type) == 'any':
                continue
            
            return False
        
        return True
    
    def visitCall(self, node: ast.Call):
        symbol = self.scope.symbol_table.tryget(node.callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'unknown callee \'{node.callee}\'')
        
        args = [cast(ast.Arg, self.visit(arg)) for arg in node.args]
        func = cast(ast.Function, symbol.value)
        arg_types = [str(arg.type) for arg in args]
        for overload in [func] + func.overloads:
            param_types = [str(param.type) for param in overload.params]
            info(f'checking call types for {overload.name} - arg_types = {arg_types}, param_types = {param_types}')
            if not self.check_args(args, overload.params):
                continue
            
            info(f'calling overload {overload.name}')
            
            new_args = []
            for arg, param in zip(args, overload.params):
                if isinstance(param.type, ast.ReferenceType):
                    if not isinstance(arg.value, ast.Id):
                        arg.pos.comptime_error(self.file, 'cannot reference non-identifier')
                    
                    ref_symbol = self.scope.symbol_table.tryget(arg.value.name)
                    if ref_symbol is None:
                        arg.pos.comptime_error(self.file, 'cannot reference unknown identifier')
                    
                    if not ref_symbol.is_mutable and param.is_mutable:
                        arg.pos.comptime_error(
                            self.file, 'argument reference symbol is immutable but is being passed by mutable reference'
                        )
                    
                    new_args.append(ast.Ref(node.pos, arg.type.reference(), arg.value.name))
                else:
                    new_args.append(arg)
            
            # TODO: check for multiple matching overloads
            return ast.Call(node.pos, overload.ret_type, overload.name, new_args)
        
        node.pos.comptime_error(self.file, f'no matching overloads for call to \'{node.callee}\'')
    
    def visitOperation(self, node: ast.Operation):
        left = self.visit(node.left)
        right = self.visit(node.right)
        callee = f'{node.op}.{left.type}.{right.type}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' between types \'{left.type}\' and \'{right.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return self.visit(ast.Call(node.pos, func.ret_type, callee, [left.to_arg(), right.to_arg()]))
    
    def visitUnaryOperation(self, node: ast.UnaryOperation):
        value = self.visit(node.value)
        callee = f'{node.op}.{value.type}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' on type \'{value.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return self.visit(ast.Call(node.pos, func.ret_type, callee, [value.to_arg()]))
    
    def visitAttribute(self, node: ast.Attribute):
        value = self.visit(node.value)
        value_type = value.type
        if value_type.is_reference():
            value_type = value_type.type
        
        callee = f'{value_type}.{node.attr}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'unknown attribute \'{node.attr}\' on type \'{value.type}\'')
        
        func = cast(ast.Function, symbol.value)
        args = [cast(ast.Arg, self.visit(arg)) for arg in node.args] if node.args is not None else []
        if not func.flags.static:
            args.insert(0, value.to_arg())
        
        return self.visit(ast.Call(node.pos, func.ret_type, callee, args))
    
    def visitNew(self, node: ast.New):
        new_type = cast(ast.Type, self.visit(node.new_type))
        callee = f'{new_type}.new'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'cannot make new type of type \'{new_type}\', no \'new\' method')
        
        func = cast(ast.Function, symbol.value)
        args = [cast(ast.Arg, self.visit(arg)) for arg in node.args]
        new_type_id = ast.Id(new_type.pos, new_type, str(new_type))
        return self.visit(ast.Attribute(node.pos, func.ret_type, new_type_id, 'new', args))
    
    def visitTernary(self, node: ast.Ternary):
        cond = self.visit(node.cond)
        true = self.visit(node.true)
        false = self.visit(node.false)
        if true.type != false.type:
            node.pos.comptime_error(self.file, f'expected branch types to match (\'{true.type}\' and \'{false.type}\')')
        
        if cond.type.type != 'bool':
            node.pos.comptime_error(self.file, 'expected condition type to be type \'bool\'')
        
        return ast.Ternary(node.pos, true.type, cond, true, false)
    
    def visitBracketed(self, node: ast.Bracketed):
        value = self.visit(node.value)
        return ast.Bracketed(node.pos, value.type, value)
