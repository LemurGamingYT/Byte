from contextlib import contextmanager
from dataclasses import dataclass
from logging import info
from typing import cast

from byte.passes import ByteCompilerPass
from byte import ast


DONT_EXTRACT = (
    ast.Type, ast.Variable, ast.Assignment, ast.If, ast.Elseif, ast.While, ast.Break, ast.Continue, ast.Id, ast.Param,
    ast.Return, ast.Function, ast.Arg, ast.Body
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
        info(f'extracted {node.__class__.__name__} with type {node.type} to temporary variable with name {var_name}')
        return var.to_id()
    
    def extract_node(self, node: ast.Node):
        if isinstance(node, DONT_EXTRACT) or not self.can_extract:
            return node

        destroy_method = self.scope.symbol_table.tryget(f'{node.type}.destroy')
        if destroy_method is None:
            return node
        
        return self.extract(node)
    
    def reached_end_of_scope(self, pos: ast.Position):
        info('reached end of scope, adding destroy calls')
        
        nodes = []
        for symbol in self.scope.symbol_table.symbols.values():
            destroy_symbol = self.scope.symbol_table.tryget(f'{symbol.type}.destroy')
            if destroy_symbol is None:
                continue
            
            destroy_func = destroy_symbol.value
            assert isinstance(destroy_func, ast.Function), f'Invalid destroy method for type {symbol.type}'
            
            if symbol.value.moved:
                info(f'{symbol.name} was moved, skipping destroy call')
                continue
            
            info(f'{symbol.name} was not moved and needs to be freed, adding destroy call')
            nodes.append(ast.Call(pos, destroy_func.ret_type, destroy_func.name, [
                ast.Id(pos, symbol.type, symbol.name).to_ref().to_arg()
            ]))
        
        return nodes
    
    def visit(self, node: ast.Node):
        return self.extract_node(super().visit(node))
    
    def visitBody(self, node: ast.Body):
        has_returned = False
        nodes = []
        for stmt in node.nodes:
            stmt = self.visit(stmt)
            if self.scope.data.prepend_nodes:
                nodes.extend(self.scope.data.prepend_nodes)
                self.scope.data.prepend_nodes = []
            
            if isinstance(stmt, ast.Return):
                nodes.extend(self.reached_end_of_scope(node.pos))
                has_returned = True
            
            nodes.append(stmt)
        
        if not has_returned:
            nodes.extend(self.reached_end_of_scope(node.pos))
        
        return ast.Body(node.pos, node.type, nodes)
    
    def visitFunction(self, node: ast.Function):
        if node.is_generic:
            return node
        
        info(f'managing memory of function body {node.name}')
        
        body = node.body
        if body is not None:
            with self.file.child_scope():
                info('adding function parameters')
                for param in node.params:
                    self.scope.symbol_table.add(ast.Symbol(param.name, param.type, OwnedObject(param, True), param.is_mutable))
                    info(f'added parameter {param.name}')
                
                body = cast(ast.Body, self.visit(body))
        
        return ast.Function(
            node.pos, node.type, node.name, node.params, body, node.flags, node.extend_type, node.generic_params, node.overloads
        )
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            info(f'variable {node.name} has an identifier as a value, attempting to set ownership')
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                info(f'{symbol.name} is now owned by {node.name}')
                
                self.scope.symbol_table.add(ast.Symbol(node.name, value.type, OwnedObject(value), node.is_mutable))
                return ast.Variable(node.pos, value.type, node.name, value, node.is_mutable, node.op)
        
        self.scope.symbol_table.add(ast.Symbol(node.name, cast(ast.Type, value.type), OwnedObject(value), node.is_mutable))
        return ast.Variable(node.pos, cast(ast.Type, value.type), node.name, value, node.is_mutable, node.op)
    
    def visitAssignment(self, node: ast.Assignment):
        assign_symbol = self.scope.symbol_table.get(node.name)
        assert assign_symbol is not None, f'Assignment symbol {node.name} not found in symbol table'
        
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            info(f'variable {node.name} has an identifier as a value, attempting to set ownership')
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                info(f'{symbol.name} is now owned by {node.name}')
                
                self.scope.symbol_table.add(ast.Symbol(node.name, value.type, OwnedObject(value), assign_symbol.is_mutable))
                return ast.Assignment(node.pos, value.type, node.name, value, node.op)
        
        self.scope.symbol_table.add(ast.Symbol(node.name, cast(ast.Type, value.type), OwnedObject(value), assign_symbol.is_mutable))
        return ast.Assignment(node.pos, cast(ast.Type, value.type), node.name, value, node.op)
    
    def visitReturn(self, node: ast.Return):
        if node.value is None:
            return node
        
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                info(f'returned an owned object instance {symbol.name}, ownership is now on the callsite')
        
        return ast.Return(node.pos, cast(ast.Type, value.type), value)
        
    def visitElseif(self, node: ast.Elseif):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        return ast.Elseif(node.pos, self.visit(node.cond), body)
    
    def visitIf(self, node: ast.If):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        else_body = node.else_body
        if else_body is not None:
            else_body = self.visitBody(else_body)
        
        return ast.If(node.pos, self.visit(node.cond), body, else_body, [self.visitElseif(elseif) for elseif in node.elseifs])
    
    def visitWhile(self, node: ast.While):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        return ast.While(node.pos, self.visit(node.cond), body)
    
    def visitForRange(self, node: ast.ForRange):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        return ast.ForRange(
            node.pos, node.iter_name, self.visit(node.start), self.visit(node.end), body,
            self.visit(node.step) if node.step is not None else None
        )
