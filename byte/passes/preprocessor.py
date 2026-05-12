from dataclasses import replace

from byte.passes import ByteCompilerPass
from byte import ast


class Preprocessor(ByteCompilerPass):
    def visitProgram(self, node: ast.Program):
        nodes = [self.visit(stmt) for stmt in node.nodes]
        nodes.insert(0, ast.Use(node.pos, 'builtins'))
        return replace(node, nodes=nodes)

    def visitClass(self, node: ast.Class):
        cls_type = self.file.type_map.add(node.name, ast.ClassType(node.name, [field.type for field in node.fields]))
        
        members = []
        for member in node.members:
            if isinstance(member, ast.Function):
                members.append(replace(member, extend_type=cls_type))
            else:
                members.append(member)

        return replace(node, members=members)
    
    def visitString(self, node: ast.String):
        return ast.Attribute(node.pos, node.type, ast.Id(node.pos, ast.Type('string'), 'string'), 'new', [
            ast.String(node.pos, self.file.type_map.get('pointer'), node.value).to_arg(),
            ast.Int(node.pos, self.file.type_map.get('int'), len(node.value)).to_arg(),
            ast.Bool(node.pos, self.file.type_map.get('bool'), False).to_arg()
        ])
