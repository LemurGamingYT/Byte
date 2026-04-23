from pathlib import Path

from byte.passes import ByteCompilerPass
from byte import ast


def test_pass_visitor():
    file = ast.File(Path.cwd() / 'examples' / 'test.byte')
    program = ast.Program(ast.Position(), [ast.Function(ast.Position(), file.type_map.get('int'), 'main', body=ast.Body(
        ast.Position(), file.type_map.get('int'), [
            ast.Return(ast.Position(), file.type_map.get('int'), ast.Int(ast.Position(), file.type_map.get('int'), 0))
        ]
    ))])
    
    expected_program = ast.Program(ast.Position(), [ast.Function(ast.Position(), file.type_map.get('int'), 'main', body=ast.Body(
        ast.Position(), file.type_map.get('int'), [
            ast.Return(ast.Position(), file.type_map.get('int'), ast.Float(ast.Position(), file.type_map.get('float'), float(0)))
        ]
    ))])
    
    test_pass = TestPass(file)
    output_program = test_pass.visit(program)
    return output_program == expected_program


class TestPass(ByteCompilerPass):
    def visitInt(self, node: ast.Int):
        return ast.Float(node.pos, self.file.type_map.get('float'), float(node.value))
