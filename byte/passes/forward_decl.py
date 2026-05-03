from byte.passes import ByteCompilerPass
from byte import ast


class ForwardDeclaration(ByteCompilerPass):
    def visitFunction(self, node: ast.Function):
        self.scope.symbol_table.add(ast.Symbol(node.name, self.file.type_map.get('function'), node, is_forward_decl=True))
        return node

    def visitClass(self, node: ast.Class):
        self.file.type_map.add(node.name)
        return node
