from logging import info
from typing import cast

from byte.llvm_extensions import Registry
from byte.passes import ByteCompilerPass
from byte import ast


def length_word(word: str, count: int):
    if count == 0:
        return f'no {word}s'
    elif count == 1:
        return f'{count} {word}'
    else:
        return f'{count} {word}s'

class TypeChecker(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)
        
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')
        Math_type = self.file.type_map.get('Math')
        
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
        
        self.declare_empty_function('print', params=[ast.Param(ast.Position(), string_type, 's')])
        
        self.declare_empty_function('string_struct', string_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), int_type, 'length')
        ])
        
        self.declare_empty_function('null_terminate', params=[
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), int_type, 'length')
        ])
        
        self.declare_empty_function('gep', pointer_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'),
            ast.Param(ast.Position(), int_type, 'offset')
        ])
        
        self.declare_attribute_function(int_type, 'to_string', string_type)
        self.declare_attribute_function(float_type, 'to_string', string_type)
        self.declare_attribute_function(string_type, 'to_string', string_type)
        self.declare_attribute_function(bool_type, 'to_string', string_type)
        
        self.declare_attribute_function(string_type, 'ptr', pointer_type, is_method=False)
        self.declare_attribute_function(string_type, 'length', int_type, is_method=False)
        
        self.declare_attribute_function(Math_type, 'sqrt', float_type, [
            ast.Param(ast.Position(), float_type, 'x')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'pow', float_type, [
            ast.Param(ast.Position(), float_type, 'base'), ast.Param(ast.Position(), float_type, 'exponent')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'abs', float_type, [
            ast.Param(ast.Position(), float_type, 'x')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'floor', int_type, [
            ast.Param(ast.Position(), float_type, 'x')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'ceil', int_type, [
            ast.Param(ast.Position(), float_type, 'x')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'min', float_type, [
            ast.Param(ast.Position(), float_type, 'a'), ast.Param(ast.Position(), float_type, 'b')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'max', float_type, [
            ast.Param(ast.Position(), float_type, 'a'), ast.Param(ast.Position(), float_type, 'b')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'imin', int_type, [
            ast.Param(ast.Position(), int_type, 'a'), ast.Param(ast.Position(), int_type, 'b')
        ], is_static=True)
        
        self.declare_attribute_function(Math_type, 'imax', int_type, [
            ast.Param(ast.Position(), int_type, 'a'), ast.Param(ast.Position(), int_type, 'b')
        ], is_static=True)
        
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
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
    
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
        else:
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
            if arg.type == param.type:
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
            
            # TODO: check for multiple matching overloads
            return ast.Call(node.pos, overload.ret_type, overload.name, args)
        
        node.pos.comptime_error(self.file, 'no matching overloads')
    
    def visitOperation(self, node: ast.Operation):
        left = self.visit(node.left)
        right = self.visit(node.right)
        callee = f'{node.op}.{left.type}.{right.type}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' between types \'{left.type}\' and \'{right.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return ast.Operation(node.pos, func.ret_type, node.op, left, right)
    
    def visitUnaryOperation(self, node: ast.UnaryOperation):
        value = self.visit(node.value)
        callee = f'{node.op}.{value.type}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' on type \'{value.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return ast.UnaryOperation(node.pos, func.ret_type, node.op, value)
    
    def visitAttribute(self, node: ast.Attribute):
        value = self.visit(node.value)
        callee = f'{value.type}.{node.attr}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'unknown attribute \'{node.attr}\' on type \'{value.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return ast.Attribute(node.pos, func.ret_type, value, node.attr, [
            cast(ast.Arg, self.visit(arg)) for arg in node.args
        ] if node.args is not None else None)
    
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
