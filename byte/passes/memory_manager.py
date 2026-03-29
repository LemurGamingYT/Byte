from contextlib import contextmanager
from dataclasses import dataclass
from typing import cast

from byte.passes import ByteCompilerPass
from byte import ast


DONT_EXTRACT = (
    ast.Type, ast.Variable, ast.Assignment, ast.If, ast.Elseif, ast.While, ast.Break, ast.Continue, ast.Id, ast.Param,
    ast.Return, ast.Function, ast.Arg
)

@dataclass
class OwnedObject:
    node: ast.Node
    moved: bool = False


class MemoryManager(ByteCompilerPass):
    def __init__(self, file: ast.File):
        super().__init__(file)
        
        self.can_extract = True
    
    @contextmanager
    def disable_extraction(self):
        self.can_extract = False
        yield
        self.can_extract = True
    
    def extract(self, node: ast.Node):
        var_name = self.file.unique_name
        var = ast.Variable(node.pos, node.type, var_name, node)
        self.scope.data.prepend_nodes.append(var)
        self.scope.symbol_table.add(ast.Symbol(var_name, var.type, OwnedObject(node)))
        return var.to_id()
    
    def extract_node(self, node: ast.Node):
        if isinstance(node, DONT_EXTRACT) or not self.can_extract:
            return node

        destroy_method = self.scope.symbol_table.tryget(f'{node.type}.destroy')
        if destroy_method is None:
            return node
        
        return self.extract(node)
    
    def reached_end_of_scope(self, pos: ast.Position):
        nodes = []
        for symbol in self.scope.symbol_table.symbols.values():
            destroy_symbol = self.scope.symbol_table.tryget(f'{symbol.type}.destroy')
            if destroy_symbol is None:
                continue
            
            destroy_func = destroy_symbol.value
            assert isinstance(destroy_func, ast.Function), f'Invalid destroy method for type {symbol.type}'
            
            if symbol.value.moved:
                continue
            
            nodes.append(ast.Call(pos, destroy_func.ret_type, destroy_func.name, [
                ast.Id(pos, symbol.type, symbol.name).to_arg()
            ]))
        
        return nodes
    
    def visit(self, node: ast.Node):
        return self.extract_node(super().visit(node))
    
    def visitBody(self, node: ast.Body):
        nodes = []
        for stmt in node.nodes:
            stmt = self.visit(stmt)
            if self.scope.data.prepend_nodes:
                nodes.extend(self.scope.data.prepend_nodes)
                self.scope.data.prepend_nodes = []
            
            if isinstance(stmt, ast.Return):
                nodes.extend(self.reached_end_of_scope(node.pos))
            
            nodes.append(stmt)
        
        return ast.Body(node.pos, node.type, nodes)
    
    def visitFunction(self, node: ast.Function):
        body = node.body
        if body is not None:
            with self.file.child_scope():
                for param in node.params:
                    self.scope.symbol_table.add(ast.Symbol(param.name, param.type, OwnedObject(param, True), param.is_mutable))
                
                body = cast(ast.Body, self.visit(body))
        
        return ast.Function(node.pos, node.type, node.name, node.params, body, node.flags, node.extend_type, node.overloads)
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                self.scope.symbol_table.add(ast.Symbol(node.name, value.type, OwnedObject(value), node.is_mutable))
                return ast.Variable(node.pos, value.type, node.name, value, node.is_mutable, node.op)
        
        self.scope.symbol_table.add(ast.Symbol(node.name, cast(ast.Type, value.type), OwnedObject(value), node.is_mutable))
        return ast.Variable(node.pos, cast(ast.Type, value.type), node.name, value, node.is_mutable, node.op)
    
    def visitAssignment(self, node: ast.Assignment):
        assign_symbol = self.scope.symbol_table.get(node.name)
        assert assign_symbol is not None, f'Assignment symbol {node.name} not found in symbol table'
        
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                self.scope.symbol_table.add(ast.Symbol(node.name, value.type, OwnedObject(value), assign_symbol.is_mutable))
                return ast.Assignment(node.pos, value.type, node.name, value, node.op)
        
        self.scope.symbol_table.add(ast.Symbol(node.name, cast(ast.Type, value.type), OwnedObject(value), assign_symbol.is_mutable))
        return ast.Assignment(node.pos, cast(ast.Type, value.type), node.name, value, node.op)
    
    def visitReturn(self, node: ast.Return):
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
        
        return ast.Return(node.pos, cast(ast.Type, value.type), value)
