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
