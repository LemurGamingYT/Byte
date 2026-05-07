from importlib import import_module
from logging import info
from typing import cast

from byte.intrinsics import intrinsic, IntrinsicCallContext
from byte.llvm_extensions import llint, NULL
from byte.passes import ByteCompilerPass
from byte import ast


class TypeChecker(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)

        self.toplevel_nodes = []
        self.expanded_generics = {}
    
    def visitProgram(self, node: ast.Program):
        for stmt in node.nodes:
            self.toplevel_nodes.append(self.visit(stmt))
        
        return ast.Program(node.pos, self.toplevel_nodes)
    
    def visitType(self, node: ast.Type):
        typ = self.file.type_map.tryget(node.type)
        if typ is None:
            node.pos.comptime_error(self.file, f'unknown type \'{node.type}\'')
        
        return typ
    
    def visitArg(self, node: ast.Arg):
        value = self.visit(node.value)
        return ast.Arg(node.pos, value.type, value)
    
    def visitParam(self, node: ast.Param):
        return ast.Param(node.pos, cast(ast.Type, self.visit(node.type)), node.name, node.flags)
    
    def visitBody(self, node: ast.Body):
        return ast.Body(node.pos, cast(ast.Type, self.visit(node.type)), [self.visit(stmt) for stmt in node.nodes])
    
    def visitReturn(self, node: ast.Return):
        if node.value is None:
            return node
        
        value = self.visit(node.value)
        return ast.Return(node.pos, value.type, value)
    
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
            extend_type = self.visit(func.extend_type)
            name = f'{extend_type}.{name}'
        
        return name
    
    def create_overload(self, base: ast.Function, func: ast.Function):
        base.overloads.append(func)
        info(f'adding new overload to {base.name}')
        
        base_param_types = [param.type for param in base.params]
        param_types = [param.type for param in func.params]
        if self.have_same_types(base_param_types, param_types):
            func.pos.comptime_error(self.file, f'an overload of {func.name} has the same types as this overload')
        
        params_mangling = '.'.join(map(str, param_types))
        mangled_name = f'{func.name}.{params_mangling}'
        info(f'mangled overload function name \'{func.name}\' to \'{mangled_name}\'')
        
        func.name = mangled_name
    
    def visitFunction(self, node: ast.Function):
        if node.is_generic:
            self.scope.symbol_table.add(ast.Symbol(node.name, self.file.type_map.get('function'), node))
            return node
        
        params = [cast(ast.Param, self.visit(param)) for param in node.params]
        ret_type = cast(ast.Type, self.visit(node.ret_type))
        extend_type = cast(ast.Type, self.visit(node.extend_type)) if node.extend_type is not None else None
        func = ast.Function(node.pos, ret_type, node.name, params, node.body, node.flags, extend_type)
        func.name = self.get_mangled_name(func)
        symbol = self.scope.symbol_table.tryget(func.name)
        if symbol is not None and not symbol.flags.forward_decl:
            base = cast(ast.Function, symbol.value)
            self.create_overload(base, func)
        
        self.scope.symbol_table.add(ast.Symbol(func.name, self.file.type_map.get('function'), func))
        if isinstance(func.body, ast.Body):
            with self.file.child_scope():
                for param in params:
                    self.scope.symbol_table.add(param.to_symbol())
                
                func.body = cast(ast.Body, self.visit(func.body))
        
        return func
    
    def visitProperty(self, node: ast.Property):
        return ast.Property(node.pos, cast(ast.Type, self.visit(node.type)), node.name)

    def init_field(self, cls_type: ast.ClassType, i: int, field: ast.Property):
        self_param = ast.Param(field.pos, cls_type, 'self')
        @intrinsic(
            None, field.type, [self_param], flags=ast.FunctionFlags(property=True),
            override_name=f'{cls_type}.{field.name}'
        )
        def getter(ctx: IntrinsicCallContext):
            struct = ctx.arg(0)
            return ctx.builder.extract_value(struct, i, field.name)

        field_get = self.visit(getattr(getter, 'ast_func'))

        self_ref_param = ast.Param(field.pos, cls_type.reference(), 'self')
        set_params = [self_ref_param, ast.Param(field.pos, field.type, 'value')]
        @intrinsic(
            None, self.file.type_map.get('nil'), set_params, flags=ast.FunctionFlags(method=True),
            override_name=f'{cls_type}.set.{field.name}'
        )
        def setter(ctx: IntrinsicCallContext):
            struct = ctx.arg(0)
            value = ctx.arg(1)
            field_ptr = ctx.builder.gep(struct, [llint(0), llint(i)], True, f'{field.name}.gep')
            ctx.builder.store(value, field_ptr)

        field_set = self.visit(getattr(setter, 'ast_func'))
        return field_get, field_set

    def init_class(self, node: ast.Class):
        cls_type = cast(ast.ClassType, self.file.type_map.get(node.name))

        fields = [member for member in node.members if isinstance(member, ast.Property)]
        constructor_params = [ast.Param(node.pos, member.type, member.name, ast.ParamFlags(copy=True)) for member in fields]
        @intrinsic(
            None, cls_type, constructor_params, flags=ast.FunctionFlags(static=True, method=True),
            override_name=f'{cls_type}.new'
        )
        def constructor(ctx: IntrinsicCallContext):
            struct_type = ctx.module.context.get_identified_type(node.name)
            return ctx.builder.struct(struct_type, ctx.codegen_args, ctx.name)

        new_constructor = self.visit(getattr(constructor, 'ast_func'))
        
        field_properties = []
        for i, field in enumerate(fields):
            field_properties.extend(self.init_field(cls_type, i, field))

        string_type = self.file.type_map.get('string')
        string_format = f'{node.name}(' + ', '.join(f'{field.name}=%.*s' for field in fields) + ')'
        
        @intrinsic(
            None, string_type, [ast.Param(node.pos, cls_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{cls_type}.to_string'
        )
        def cls_to_string(ctx: IntrinsicCallContext):
            from llvmlite import ir
            
            asprintf = ctx.module.registry.get('asprintf')

            struct = ctx.arg(0)
            field_strs = []
            for i, field in enumerate(fields):
                field_value = ctx.builder.extract_value(struct, i, field.name)
                field_str = ctx.call(f'{field.type}.to_string', [
                    ast.Arg(ctx.pos, field.type, field_value)
                ])
                field_strs.append(field_str)

            buf_addr = ctx.builder.alloca(ir.PointerType(ir.IntType(8)))
            ctx.builder.store(NULL(), buf_addr)

            fmt = ctx.module.try_get_global(
                f'{node.name}_str_fmt', lambda: ctx.module.global_string(string_format, f'{node.name}_str_fmt')
            )
            fmt_ptr = ctx.builder.first_elem(fmt, 'fmt_ptr')

            asprintf_args = [buf_addr, fmt_ptr]
            for field_str in field_strs:
                length = ctx.call('string.length', [ast.Arg(ctx.pos, ctx.file.type_map.get('string'), field_str)])
                ptr = ctx.call('string.ptr', [ast.Arg(ctx.pos, ctx.file.type_map.get('string'), field_str)])
                asprintf_args.append(length)
                asprintf_args.append(ptr)

            written = ctx.builder.call(asprintf, asprintf_args, 'written')
            return ctx.call('string.new', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), ctx.builder.load(buf_addr, 'buf')),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), written),
                ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(1, 1))
            ])

        to_string = self.visit(getattr(cls_to_string, 'ast_func'))

        return [new_constructor, to_string] + field_properties
    
    def visitClass(self, node: ast.Class):
        field_types = [field.type for field in node.fields]
        self.file.type_map.add(node.name, ast.ClassType(node.name, field_types))
        
        members = self.init_class(node)
        for member in node.members:
            if isinstance(member, ast.Function):
                member.extend_type = self.file.type_map.get(node.name)
            
            members.append(self.visit(member))

        return ast.Class(node.pos, node.name, cast(list[ast.Function | ast.Property], members))
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        if self.scope.symbol_table.has(node.name):
            return self.visit(ast.Assignment(node.pos, value.type, node.name, value, node.op))
        
        self.scope.symbol_table.add(ast.Symbol(node.name, value.type, value, ast.SymbolFlags(mutable=node.is_mutable)))
        return ast.Variable(node.pos, value.type, node.name, value, node.is_mutable)
    
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
        if node.op is not None:
            value = self.visit(ast.Operation(
                node.value.pos, node.type, node.op, ast.Id(node.pos, node.type, node.name), node.value
            ))

        if node.attr is not None:
            var_id = ast.Id(node.pos, value.type, node.name)
            return self.visit(ast.Attribute(
                node.pos, self.file.type_map.get('nil'), var_id, f'set.{node.attr}', [value.to_arg()]
            ))
        
        return ast.Assignment(node.pos, value.type, node.name, value)
    
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
            body = cast(ast.Body, self.visit(node.body))
        
        return ast.While(node.pos, self.visit(node.cond), body)
    
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
        
        return ast.ForRange(node.pos, node.iter_name, start, end, body, step)
    
    def use_py(self, file: ast.File, path: str):
        stdlib_path = ast.STDLIB_PATH / f'{path}.py'
        if not stdlib_path.exists():
            return False

        module = import_module(f'byte.stdlib.{path}')
        cls = getattr(module, path)
        instance = cls(file)
        instance.init()
        for k, v in instance.intrinsics.items():
            ast_func = v.ast_func
            file.scope.symbol_table.add(ast.Symbol(k, self.file.type_map.get('function'), ast_func))
            self.scope.symbol_table.add(ast.Symbol(k, self.file.type_map.get('function'), ast_func))
        
        return True

    def use_byte(self, file: ast.File, path: str):
        from byte import Pipeline

        if self.file.path.stem == file.path.stem:
            return True

        stdlib_path = ast.STDLIB_PATH / f'{path}.byte'
        if not stdlib_path.exists():
            return False

        file.path = stdlib_path
        pipeline = Pipeline()
        pipeline.end_at_pass(TypeChecker).run_passes(file)
        
        self.scope.symbol_table.merge(file.scope.symbol_table)
        self.file.type_map.merge(file.type_map)
        return True

    def visitUse(self, node: ast.Use):
        file = ast.File(ast.STDLIB_PATH / node.path, options=self.file.options, target=self.file.target)
        used_py = self.use_py(file, node.path)
        used_byte = self.use_byte(file, node.path)
        if not used_py and not used_byte:
            node.pos.comptime_error(self.file, f'unknown library \'{node.path}\'')
        
        return node
    
    def visitId(self, node: ast.Id):
        symbol = self.scope.symbol_table.tryget(node.name)
        typ = self.file.type_map.tryget(node.name)
        return ast.Id(node.pos, symbol.type if symbol is not None else cast(ast.Type, typ), node.name)
    
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
            if not param.type.is_reference():
                continue

            if not isinstance(arg.value, (ast.Ref, ast.Deref, ast.Id)):
                # TODO: turn argument into a temporary variable
                arg.pos.comptime_error(self.file, 'cannot reference non-identifier')
            
            ref_symbol = self.scope.symbol_table.tryget(arg.value.name)
            if ref_symbol is None:
                arg.pos.comptime_error(self.file, 'cannot reference unknown identifier')
            
            if not ref_symbol.flags.mutable and param.flags.mutable:
                arg.pos.comptime_warning(
                    self.file, f"""argument reference symbol is immutable but is being passed by mutable reference
make {ref_symbol.name} mutable using the 'mut' keyword to remove this warning""")

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
        
        params = [
            ast.Param(param.pos, generic_map.get(str(param.type), param.type), param.name, param.flags)
            for param in func.params
        ]
        
        generic_name = f'{func.name}{generic_params_str}'
        if generic_name in self.expanded_generics:
            info(f'reusing expanded generic {generic_name}')
            return self.expanded_generics[generic_name]
        
        generic_func = self.visitFunction(ast.Function(
            func.pos, generic_map.get(str(func.type), func.type), generic_name, params, func.body, func.flags,
            func.extend_type, overloads=func.overloads
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
        arg_types = [str(arg.type) for arg in args]
        for overload in [func] + func.overloads:
            param_types = [str(param.type) for param in overload.params]
            info(f'checking call types for {overload.name} - arg_types = {arg_types}, param_types = {param_types}')
            if not self.check_args(args, overload):
                continue
            
            info(f'calling overload {overload.name}')
            self.fix_args(overload, args)
            overload = self.instantiate_generics(overload, args)
            return ast.Call(node.pos, overload.ret_type, overload.name, args)

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
