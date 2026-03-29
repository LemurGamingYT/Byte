from pathlib import Path

from byte import ast


def test_scopes():
    file = ast.File(Path.cwd() / 'examples' / 'test.byte')
    int_type = file.type_map.get('int')
    file.scope.symbol_table.add(ast.Symbol('a', int_type, ast.Int(ast.Position(), int_type, 20)))
    assert file.scope.symbol_table.has('a')
    
    with file.child_scope():
        assert file.scope.symbol_table.has('a')
        
        file.scope.symbol_table.add(ast.Symbol('b', int_type, ast.Int(ast.Position(), int_type, 42)))
        assert file.scope.symbol_table.has('b')
    
    assert not file.scope.symbol_table.has('b')
