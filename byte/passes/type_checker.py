from dataclasses import replace
from logging import error, info
from typing import cast

from byte.passes import ByteCompilerPass
from byte.classes import init_class
from byte import ast


class TypeChecker(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)

        self.toplevel_nodes = []
        self.expanded_generics = {}
    
    def visitProgram(self, node: ast.Program):
        for stmt in node.nodes:
            self.toplevel_nodes.append(self.visit(stmt))
        
        return replace(node, nodes=self.toplevel_nodes)
    
    def visitType(self, node: ast.Type):
        typ = self.file.type_map.tryget(node.type)
        if typ is None:
            node.pos.comptime_error(self.file, f'unknown type \'{node.type}\'')
        
        return typ

    def visitReferenceType(self, node: ast.ReferenceType):
        return replace(node, type=self.visit(node.type))
    
    def visitArg(self, node: ast.Arg):
        value = self.visit(node.value)
        return replace(node, type=value.type, value=value)
    
    def visitParam(self, node: ast.Param):
        return replace(node, type=self.visit(node.type))
    
    def visitBody(self, node: ast.Body):
        nodes = []
        for stmt in node.nodes:
            stmt = self.visit(stmt)
            if self.scope.data.prepend_nodes:
                nodes.extend(self.scope.data.prepend_nodes)
                self.scope.data.prepend_nodes.clear()

            nodes.append(stmt)
        
        return replace(node, type=self.visit(node.type), nodes=nodes)
    
    def visitReturn(self, node: ast.Return):
        if node.value is None:
            return node
        
        value = self.visit(node.value)
        return replace(node, type=value.type, value=value)
    
    def have_same_types(self, list1: list[ast.Type], list2: list[ast.Type]):
        if len(list1) != len(list2):
            return False
        
        return all(type1 == type2 for type1, type2 in zip(list1, list2))
    
    def get_mangled_name(self, func: ast.Function):
        name = func.name
        if name in ('+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&&', '||'):
            if len(func.params) != 2:
                func.pos.comptime_error(self.file, f'operator overload of \'{name}\' must have two parameters')
            
            a, b = func.params
            name = f'{name}.{a.type}.{b.type}'
        elif name == '!':
            if len(func.params) != 1:
                func.pos.comptime_error(self.file, f'operator overload of \'{name}\' must have one parameter')
            
            a = func.params[0]
            name = f'{name}.{a.type}'
        
        if func.extend_type is not None:
            name = f'{func.extend_type}.{name}'
        
        return name
    
    def create_overload(self, base: ast.Function, func: ast.Function):
        info(f'adding new overload to {base.name}')
        
        base_param_types = [param.type for param in base.params]
        param_types = [param.type for param in func.params]
        if self.have_same_types(base_param_types, param_types):
            func.pos.comptime_error(self.file, f'an overload of {func.name} has the same types as this overload')
        
        params_mangling = '.'.join(map(str, param_types))
        mangled_name = f'{func.name}.{params_mangling}'
        info(f'mangled overload function name \'{func.name}\' to \'{mangled_name}\'')

        overload = replace(func, name=mangled_name)
        base.overloads.append(overload)
        return overload
    
    def visitFunction(self, node: ast.Function):
        if node.is_generic:
            self.scope.symbol_table.add(ast.Symbol(node.name, self.file.type_map.get('function'), node))
            return node
        
        params = [self.visit(param) for param in node.params]
        ret_type = cast(ast.Type, self.visit(node.ret_type))
        if ret_type.is_reference():
            node.pos.comptime_error(self.file, 'return type cannot be a reference')
        
        extend_type = self.visit(node.extend_type) if node.extend_type is not None else None
        func = replace(node, type=ret_type, params=params, extend_type=extend_type)
        func = replace(func, name=self.get_mangled_name(func))
        symbol = self.scope.symbol_table.tryget(func.name)
        if symbol is not None and not symbol.flags.forward_decl:
            base = cast(ast.Function, symbol.value)
            func = self.create_overload(base, func)
        
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
        if isinstance(func.body, ast.Body):
            with self.file.child_scope():
                for param in params:
                    self.scope.symbol_table.add(cast(ast.Param, param).to_symbol())

                func = replace(func, body=self.visit(func.body))
        
        return func
    
    def visitProperty(self, node: ast.Property):
        return replace(node, type=self.visit(node.type))

    def visitField(self, node: ast.Field):
        return replace(node, type=self.visit(node.type))
    
    def visitClass(self, node: ast.Class):
        new_members = []
        fields = [cast(ast.Field, self.visit(f)) for f in node.fields]
        field_types = [field.type for field in fields]
        self.file.type_map.add(node.name, ast.ClassType(node.name, field_types))
        
        members = init_class(node.pos, self.file, node.name, fields) + node.members
        for member in members:
            new_members.append(self.visit(member))

        return replace(node, members=new_members)
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        if self.scope.symbol_table.has(node.name):
            return self.visit(ast.Assignment(node.pos, value.type, node.name, value, node.op))
        
        self.scope.symbol_table.add(ast.Symbol(node.name, value.type, value, ast.SymbolFlags(mutable=node.is_mutable)))
        return replace(node, type=value.type, value=value)
    
    def visitAssignment(self, node: ast.Assignment):
        symbol = self.scope.symbol_table.tryget(node.name)
        if symbol is None:
            node.pos.comptime_error(self.file, f'unknown symbol \'{node.name}\'')

        if not symbol.flags.mutable:
            if node.attr is not None:
                node.pos.comptime_error(
                    self.file, f'cannot change attribute \'{node.attr}\' because \'{node.name}\' is immutable'
                )
            
            node.pos.comptime_error(self.file, f'\'{node.name}\' is immutable')
        
        value = node.value
        var_id = ast.Id(node.pos, node.type, node.name)
        if node.op is not None:
            left = var_id
            if node.attr is not None:
                left = self.visit(ast.Attribute(
                    node.pos, self.file.type_map.get('nil'), var_id, node.attr
                ))
            
            value = self.visit(ast.Operation(value.pos, node.type, node.op, left, value))

        if node.attr is not None:
            return self.visit(ast.Attribute(
                node.pos, self.file.type_map.get('nil'), var_id, f'set.{node.attr}', [value.to_arg()]
            ))
        
        return replace(node, type=value.type, value=value)
    
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
        
        return replace(node, cond=self.visit(node.cond), body=body, else_body=else_body, elseifs=[
            self.visit(elseif) for elseif in node.elseifs
        ])
    
    def visitWhile(self, node: ast.While):
        with self.file.child_scope():
            body = cast(ast.Body, self.visit(node.body))
        
        return replace(node, cond=self.visit(node.cond), body=body)
    
    def is_valid_range_type(self, type: ast.Type):
        return str(type) in ('int', 'float')
    
    def determine_step_value(self, pos: ast.Position, type: ast.Type):
        if str(type) == 'int':
            return ast.Int(pos, self.file.type_map.get('int'), 1)
        elif str(type) == 'float':
            return ast.Float(pos, self.file.type_map.get('float'), 1.0)
        
        raise NotImplementedError(str(type))
    
    def visitForRange(self, node: ast.ForRange):
        start = self.visit(node.start)
        end = self.visit(node.end)
        step = self.visit(node.step) if node.step is not None else None
        if not self.is_valid_range_type(start.type):
            start.pos.comptime_error(self.file, f'invalid range type \'{start.type}\'')
        
        if not self.is_valid_range_type(end.type):
            end.pos.comptime_error(self.file, f'invalid range type \'{end.type}\'')
        
        if start.type != end.type:
            start.pos.comptime_error(self.file, f'range start and end types do not match (\'{start.type}\' and \'{end.type}\')')
        
        if step is not None and not self.is_valid_range_type(step.type):
            step.pos.comptime_error(self.file, f'invalid range type \'{step.type}\'')
        
        if step is None:
            step = self.determine_step_value(node.pos, start.type)
        
        with self.file.child_scope():
            self.scope.symbol_table.add(ast.Symbol(node.iter_name, start.type, step))

            body = cast(ast.Body, self.visit(node.body))
        
        return replace(node, start=start, end=end, body=body, step=step)

    def visitForeach(self, node: ast.Foreach):
        value = cast(ast.Node, self.visit(node.value))
        iter_at_symbol = self.scope.symbol_table.tryget(f'{value.type.basic_type}.iter.at')
        iter_len_symbol = self.scope.symbol_table.tryget(f'{value.type.basic_type}.iter.len')
        if iter_at_symbol is None or iter_len_symbol is None:
            value.pos.comptime_error(self.file, f'invalid type \'{value.type}\' for foreach')

        iter_at_func = cast(ast.Function, iter_at_symbol.value)
        iter_len_func = cast(ast.Function, iter_len_symbol.value)
        idx_name = self.file.unique_name
        idx_var = ast.Id(value.pos, self.file.type_map.get('int'), idx_name)
        body_nodes = [ast.Variable(node.body.pos, iter_at_func.ret_type, node.iter_name, ast.Call(
            node.body.pos, iter_at_func.ret_type, iter_at_func.name, [value.to_arg(), idx_var.to_arg()]
        ))] + node.body.nodes
        start = ast.Int(node.pos, self.file.type_map.get('int'), 0)
        end = ast.Call(value.pos, iter_len_func.ret_type, iter_len_func.name, [value.to_arg()])
        return self.visit(ast.ForRange(node.pos, idx_name, start, end, replace(node.body, nodes=body_nodes)))

    def visitUse(self, node: ast.Use):
        stdlib_path = ast.STDLIB_PATH / node.path
        file = ast.File(stdlib_path, options=self.file.options, target=self.file.target)
        if stdlib_path.is_dir():
            std_py_file = stdlib_path / f'{node.path}.byte'
            if std_py_file.exists():
                node.use_py_file(file, self.file, std_py_file)
            else:
                for py_file in stdlib_path.rglob('*.py'):
                    node.use_py_file(file, self.file, py_file)

            std_byte_file = stdlib_path / f'{node.path}.byte'
            if std_byte_file.exists():
                node.use_byte_file(file, self.file, std_byte_file, TypeChecker)
            else:
                for byte_file in stdlib_path.rglob('*.byte'):
                    node.use_byte_file(file, self.file, byte_file, TypeChecker)
        else:
            py_file = ast.STDLIB_PATH / f'{node.path}.py'
            if py_file.exists():
                node.use_py_file(file, self.file, py_file)

            byte_file = ast.STDLIB_PATH / f'{node.path}.byte'
            if byte_file.exists():
                node.use_byte_file(file, self.file, byte_file, TypeChecker)

            if not py_file.exists() and not byte_file.exists():
                node.pos.comptime_error(self.file, f'unknown library \'{node.path}\'')
        
        return node
    
    def visitId(self, node: ast.Id):
        symbol = self.scope.symbol_table.tryget(node.name)
        typ = self.file.type_map.tryget(node.name)
        return replace(node, type=symbol.type if symbol is not None else typ)
    
    def check_args(self, args: list[ast.Arg], func: ast.Function):
        params = func.params
        if len(args) != len(params):
            return False
        
        for arg, param in zip(args, params):
            if arg.type == param.type or str(param.type) == 'any' or str(param.type) in func.generic_params:
                continue
            
            return False
        
        return True
    
    def fix_args(self, overload: ast.Function, args: list[ast.Arg]):
        for i, (arg, param) in enumerate(zip(args, overload.params)):
            # TODO: fix when the arg type is a reference and the param type is not a reference
            # (this breaks intrinsic python code because it doesn't expect a pointer type but receives one)
            if not param.type.is_reference():# and not arg.type.is_reference():
                continue

            if not isinstance(arg.value, (ast.Ref, ast.Deref, ast.Id)):
                temp_name = self.file.unique_name
                self.scope.data.prepend_nodes.append(ast.Variable(
                    arg.pos, arg.type, temp_name, arg.value
                ))

                arg.value = ast.Id(arg.pos, arg.type, temp_name)
                self.scope.symbol_table.add(ast.Symbol(temp_name, arg.type, arg.value))
            
            ref_symbol = self.scope.symbol_table.tryget(arg.value.name)
            if ref_symbol is None:
                arg.pos.comptime_error(self.file, 'cannot reference unknown identifier')
            
            if not ref_symbol.flags.mutable and param.flags.mutable:
                arg.pos.comptime_error(self.file, 'argument reference symbol is immutable but is being passed by mutable reference')

            if ref_symbol.type.is_reference():
                args[i] = ast.Deref(arg.pos, arg.type, arg.value.name).to_arg()
                continue
            
            args[i] = ast.Ref(arg.pos, arg.type.reference(), arg.value.name).to_arg()
    
    def create_generic_map(self, func: ast.Function, args: list[ast.Arg]):
        generic_map = {}
        for arg, param in zip(args, func.params):
            generic_param = str(param.type)
            if generic_param not in func.generic_params:
                continue
            
            if generic_param in generic_map:
                generic_type = generic_map[generic_param]
                if generic_type != arg.type:
                    arg.pos.comptime_error(self.file, 'mismatched generic types in call')
                
                continue
            
            generic_map[generic_param] = arg.type
        
        return generic_map
    
    def instantiate_generics(self, func: ast.Function, args: list[ast.Arg]):
        if not func.is_generic:
            return func
        
        arg_types = [str(arg.type) for arg in args]
        info(f'instantiating new generic function {func.name} with types {arg_types}')
        generic_map = self.create_generic_map(func, args)
        generic_params_str = '<' + ', '.join(str(generic_type) for generic_type in generic_map.values()) + '>'
        
        generic_name = f'{func.name}{generic_params_str}'
        if generic_name in self.expanded_generics:
            info(f'reusing expanded generic {generic_name}')
            return self.expanded_generics[generic_name]
        
        params = [
            ast.Param(param.pos, generic_map.get(str(param.type), param.type), param.name, param.flags)
            for param in func.params
        ]
        
        generic_func = self.visitFunction(replace(
            func, type=generic_map.get(str(func.type), func.type), name=generic_name, params=params,
            generic_params=[]
        ))
        
        self.expanded_generics[generic_name] = generic_func
        
        func.overloads.append(generic_func)
        
        try:
            idx = self.toplevel_nodes.index(func)
        except ValueError:
            idx = len(self.toplevel_nodes) - 1
        
        self.toplevel_nodes.insert(idx + 1, generic_func)
        info(f'inserted new instantiated generic at index {idx} in top-level node list')
        info(f'created new generic function with signature \'{generic_func.signature}\'')
        return generic_func
    
    def visitCall(self, node: ast.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        args = [cast(ast.Arg, self.visit(arg)) for arg in node.args]
        func = cast(ast.Function, symbol.value)
        for overload in [func] + func.overloads:
            if not self.check_args(args, overload):
                continue
            
            info(f'calling overload {overload.name}')
            self.fix_args(overload, args)
            overload = self.instantiate_generics(overload, args)
            return ast.Call(node.pos, overload.ret_type, overload.name, args)

        overload_param_types = []
        for overload in [func] + func.overloads:
            param_type_names = ', '.join(f'{param.type} ({param.type.__class__.__name__})' for param in overload.params)
            overload_param_types.append(f'   {overload.name}: ({param_type_names}) -> {overload.ret_type}')

        arg_types = ', '.join(f'{arg.type} ({arg.type.__class__.__name__})' for arg in args)
        error(f'attempt to call {node.callee} has no overload with arg types {arg_types}, possible overloads:\n'\
            + '\n'.join(overload_param_types))
        node.pos.comptime_error(self.file, f'no matching overloads for call to \'{node.callee}\'')
    
    def visitOperation(self, node: ast.Operation):
        left = self.visit(node.left)
        right = self.visit(node.right)
        callee = f'{node.op}.{left.type.basic_type}.{right.type.basic_type}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' between types \'{left.type}\' and \'{right.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return self.visit(ast.Call(node.pos, func.ret_type, callee, [left.to_arg(), right.to_arg()]))
    
    def visitUnaryOperation(self, node: ast.UnaryOperation):
        value = self.visit(node.value)
        callee = f'{node.op}.{value.type.basic_type}'
        symbol = self.scope.symbol_table.tryget(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' on type \'{value.type}\'')
        
        func = cast(ast.Function, symbol.value)
        return self.visit(ast.Call(node.pos, func.ret_type, callee, [value.to_arg()]))
    
    def visitAttribute(self, node: ast.Attribute):
        value = self.visit(node.value)
        callee = f'{value.type.basic_type}.{node.attr}'
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
        
        if str(cond.type) != 'bool':
            node.pos.comptime_error(self.file, 'expected condition type to be type \'bool\'')
        
        return ast.Ternary(node.pos, true.type, cond, true, false)
    
    def visitBracketed(self, node: ast.Bracketed):
        value = self.visit(node.value)
        return ast.Bracketed(node.pos, value.type, value)
