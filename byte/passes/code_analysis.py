from byte.passes import ByteCompilerPass
from byte import ast


class CodeAnalysis(ByteCompilerPass):
    def visitBody(self, node: ast.Body):
        for i, stmt in enumerate(node.nodes):
            if isinstance(stmt, (ast.Return, ast.Break, ast.Continue)) and len(node.nodes) - 1 > i:
                next_node = node.nodes[i + 1]
                next_node.pos.comptime_warning(self.file, 'unreachable code')
                break
            
            self.visit(stmt)
        
        return node

    def visitWhile(self, node: ast.While):
        with self.file.child_scope():
            self.scope.in_loop = True

            self.visit(node.body)

        return node

    def visitForRange(self, node: ast.ForRange):
        with self.file.child_scope():
            self.scope.in_loop = True

            self.visit(node.body)

        return node

    def visitBreak(self, node: ast.Break):
        if not self.scope.in_loop:
            node.pos.comptime_error(self.file, 'break statement used outside a loop')

        return node

    def visitContinue(self, node: ast.Continue):
        if not self.scope.in_loop:
            node.pos.comptime_error(self.file, 'continue statement used outside a loop')

        return node
