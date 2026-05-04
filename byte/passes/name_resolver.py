from importlib import import_module

from byte.passes import ByteCompilerPass
from byte.intrinsics import Intrinsics
from byte import ast


class NameResolver(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)

        self.intrinsics = Intrinsics(file)

    def visitFunction(self, node: ast.Function):
        if node.body is not None:
            with self.file.child_scope():
                for param in node.params:
                    self.scope.symbol_table.add(param.to_symbol())
    
                self.visit(node.body)

        return node

    def visitVariable(self, node: ast.Variable):
        self.scope.symbol_table.add(ast.Symbol(node.name, node.type, node.value, node.is_mutable))
        return node

    def visitIf(self, node: ast.If):
        with self.file.child_scope():
            self.visit(node.body)

        if node.else_body is not None:
            with self.file.child_scope():
                self.visit(node.body)

        for elseif in node.elseifs:
            with self.file.child_scope():
                self.visit(elseif.body)

        return node

    def visitWhile(self, node: ast.While):
        with self.file.child_scope():
            self.visit(node.body)

        return node

    def visitForRange(self, node: ast.ForRange):
        if self.scope.symbol_table.has(node.iter_name):
            node.pos.comptime_error(self.file, f'name \'{node.iter_name}\' already in use')
        
        with self.file.child_scope():
            self.scope.symbol_table.add(ast.Symbol(node.iter_name, node.type, node))

            self.visit(node.body)

        return node

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
        from byte import run_passes, PASS_CLASSES

        if self.file.path.stem == file.path.stem:
            return True
        
        stdlib_path = ast.STDLIB_PATH / f'{path}.byte'
        if not stdlib_path.exists():
            return False

        file.path = stdlib_path
        run_passes(file, PASS_CLASSES.index(NameResolver) + 1)
        
        self.scope.symbol_table.merge(file.scope.symbol_table)
        self.file.type_map.merge(file.type_map)
        return True

    def visitUse(self, node: ast.Use):
        if node.path == 'intrinsics':
            self.intrinsics.register()
            return node

        file = ast.File(ast.STDLIB_PATH / node.path, options=self.file.options, target=self.file.target)
        used_py = self.use_py(file, node.path)
        used_byte = self.use_byte(file, node.path)
        if not used_py and not used_byte:
            node.pos.comptime_error(self.file, f'unknown library \'{node.path}\'')
        
        return node

    def visitId(self, node: ast.Id):
        symbol = self.scope.symbol_table.tryget(node.name)
        typ = self.file.type_map.tryget(node.name)
        if symbol is None and typ is None:
            node.pos.comptime_error(self.file, f'unknown identifier \'{node.name}\'')
        
        return node

    def visitCall(self, node: ast.Call):
        symbol = self.scope.symbol_table.tryget(node.callee)
        if symbol is None:
            if self.file.type_map.has(node.callee):
                node.pos.comptime_error(
                    self.file,
                    f'unknown callee \'{node.callee}\' ({node.callee} is a type, '\
                    'did you mean to create it with \'new\'?)'
                )
            
            node.pos.comptime_error(self.file, f'unknown callee \'{node.callee}\'')

        return node
