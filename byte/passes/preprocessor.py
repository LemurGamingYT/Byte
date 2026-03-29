from byte.passes import ByteCompilerPass
from byte import ast


class Preprocessor(ByteCompilerPass):
    def visitProgram(self, node: ast.Program):
        nodes = [self.visit(stmt) for stmt in node.nodes]
        if self.file.path.stem != 'builtins':
            nodes.insert(0, ast.Use(node.pos, 'builtins'))
        
        return ast.Program(node.pos, nodes)
    
    def visitString(self, node: ast.String):
        return ast.Attribute(node.pos, node.type, ast.Type('string'), 'new', [
            ast.String(node.pos, self.file.type_map.get('pointer'), node.value).to_arg(),
            ast.Int(node.pos, self.file.type_map.get('int'), len(node.value)).to_arg()
        ])
