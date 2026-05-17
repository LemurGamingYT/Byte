from importlib import import_module
from pathlib import Path

from byte.passes import ByteCompilerPass
from byte import ast


class NameResolver(ByteCompilerPass):
    def visitFunction(self, node: ast.Function):
        if isinstance(node.body, ast.Body):
            with self.file.child_scope():
                for param in node.params:
                    self.scope.symbol_table.add(param.to_symbol())
    
                self.visit(node.body)

        return node

    def visitVariable(self, node: ast.Variable):
        self.scope.symbol_table.add(ast.Symbol(node.name, node.type, node.value, ast.SymbolFlags(mutable=node.is_mutable)))
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

    def visitForeach(self, node: ast.Foreach):
        if self.scope.symbol_table.has(node.iter_name):
            node.pos.comptime_error(self.file, f'name \'{node.iter_name}\' already in use')

        with self.file.child_scope():
            self.scope.symbol_table.add(ast.Symbol(node.iter_name, node.type, node))

            self.visit(node.body)

        return node

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
                node.use_byte_file(file, self.file, std_byte_file, NameResolver)
            else:
                for byte_file in stdlib_path.rglob('*.byte'):
                    node.use_byte_file(file, self.file, byte_file, NameResolver)
        else:
            py_file = ast.STDLIB_PATH / f'{node.path}.py'
            if py_file.exists():
                node.use_py_file(file, self.file, py_file)

            byte_file = ast.STDLIB_PATH / f'{node.path}.byte'
            if byte_file.exists():
                node.use_byte_file(file, self.file, byte_file, NameResolver)

            if not py_file.exists() and not byte_file.exists():
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
