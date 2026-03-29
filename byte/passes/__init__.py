from dataclasses import fields
from abc import ABC

from byte import ast


class ByteCompilerPass(ABC):
    def __init__(self, file: ast.File):
        self.file = file
    
    @property
    def scope(self):
        return self.file.scope
    
    @scope.setter
    def scope_setter(self, scope: ast.Scope):
        self.file.scope = scope
    
    @classmethod
    def run(cls, file: ast.File, node: ast.Node):
        return cls(file).visit(node)
    
    def visit(self, node: ast.Node):
        node_type = type(node).__name__
        method_name = f'visit{node_type}'
        method = getattr(self, method_name, None)
        if method is None:
            return self.visit_children(node)
        
        return method(node)
    
    def visit_children(self, node: ast.Node):
        args = []
        for field in fields(node):
            if not field.init:
                continue
            
            value = getattr(node, field.name)
            if isinstance(value, ast.Node):
                args.append(self.visit(value))
            elif isinstance(value, list):
                args.append([self.visit(elem) for elem in value if isinstance(elem, ast.Node)])
            else:
                args.append(value)
        
        return node.__class__(*args)
