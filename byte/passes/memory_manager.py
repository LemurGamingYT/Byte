from dataclasses import dataclass, replace
from contextlib import contextmanager
from logging import info
from typing import cast

from byte.passes import ByteCompilerPass
from byte import ast


DONT_EXTRACT = (
    ast.Type, ast.Variable, ast.Assignment, ast.If, ast.Elseif, ast.While, ast.Break, ast.Continue, ast.Id, ast.Param,
    ast.Return, ast.Function, ast.Arg, ast.Body, ast.Property
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

    def can_extract_node(self, node: ast.Node):
        if not self.can_extract:
            return False

        if isinstance(node, ast.Call):
            symbol = self.scope.symbol_table.get(node.callee)
            func = cast(ast.Function, symbol.value)
            if func.flags.returns_reference:
                return False

        return True
    
    def extract(self, node: ast.Node):
        var_name = self.file.unique_name
        var = ast.Variable(node.pos, node.type, var_name, node)
        self.scope.data.prepend_nodes.append(var)
        self.scope.symbol_table.add(ast.Symbol(var_name, var.type, OwnedObject(node)))
        info(f'extracted {node.__class__.__name__} with type {node.type} to temporary variable with name {var_name}')
        return var.to_id()
    
    def extract_node(self, node: ast.Node):
        if isinstance(node, DONT_EXTRACT) or not self.can_extract_node(node):
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
        
        return replace(node, nodes=nodes)
    
    def visitFunction(self, node: ast.Function):
        if node.is_generic:
            return node
        
        info(f'managing memory of function body {node.name}')
        
        body = node.body
        if isinstance(body, ast.Body):
            with self.file.child_scope():
                info('adding function parameters')
                for param in node.params:
                    self.scope.symbol_table.add(ast.Symbol(
                        param.name, param.type, OwnedObject(param, True), ast.SymbolFlags(mutable=param.flags.mutable)
                    ))
                    
                    info(f'added parameter {param.name}')
                
                body = cast(ast.Body, self.visit(body))

        self.scope.symbol_table.add(ast.Symbol(
            node.name, self.file.type_map.get('function'), node
        ))
        
        return replace(node, body=body)
    
    def visitVariable(self, node: ast.Variable):
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            info(f'variable {node.name} has an identifier as a value, attempting to set ownership')
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                info(f'{symbol.name} is now owned by {node.name}')
                
                self.scope.symbol_table.add(ast.Symbol(
                    node.name, value.type, OwnedObject(value), ast.SymbolFlags(mutable=node.is_mutable)
                ))
                
                return replace(node, type=value.type, value=value)
        
        self.scope.symbol_table.add(ast.Symbol(
            node.name, cast(ast.Type, value.type), OwnedObject(value), ast.SymbolFlags(mutable=node.is_mutable)
        ))
        
        return replace(node, type=value.type, value=value)
    
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
                
                self.scope.symbol_table.add(ast.Symbol(
                    node.name, value.type, OwnedObject(value), ast.SymbolFlags(mutable=assign_symbol.flags.mutable)
                ))
                
                return replace(node, type=value.type, value=value)
        
        self.scope.symbol_table.add(ast.Symbol(
            node.name, cast(ast.Type, value.type), OwnedObject(value), ast.SymbolFlags(mutable=assign_symbol.flags.mutable)
        ))
        
        return replace(node, type=value.type, value=value)
    
    def visitReturn(self, node: ast.Return):
        if node.value is None:
            return node
        
        value = self.visit(node.value)
        if isinstance(value, ast.Id):
            symbol = self.scope.symbol_table.get(value.name)
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
                info(f'returned an owned object instance {symbol.name}, ownership is now on the callsite')
        
        return replace(node, type=value.type, value=value)
        
    def visitElseif(self, node: ast.Elseif):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        return replace(node, cond=self.visit(node.cond), body=body)
    
    def visitIf(self, node: ast.If):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        else_body = node.else_body
        if else_body is not None:
            with self.file.child_scope():
                else_body = self.visitBody(else_body)
        
        return replace(
            node, cond=self.visit(node.cond), body=body, else_body=else_body,
            elseifs=[self.visit(elseif) for elseif in node.elseifs]
        )
    
    def visitWhile(self, node: ast.While):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        return replace(node, cond=self.visit(node.cond), body=body)
    
    def visitForRange(self, node: ast.ForRange):
        with self.file.child_scope():
            body = self.visitBody(node.body)
        
        return replace(
            node, start=self.visit(node.start), end=self.visit(node.end), body=body,
            step=self.visit(node.step) if node.step is not None else None
        )

    def clone_arg(self, arg: ast.Arg):
        clone_method_name = f'{arg.type}.clone'
        clone_method_symbol = self.scope.symbol_table.tryget(clone_method_name)
        if clone_method_symbol is None:
            return arg

        clone_method = cast(ast.Function, clone_method_symbol.value)
        return ast.Call(arg.pos, clone_method.ret_type, clone_method.name, [arg])

    def visitCall(self, node: ast.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        func = cast(ast.Function, symbol.value)
        args = []
        for arg, param in zip(node.args, func.params):
            arg = cast(ast.Arg, self.visit(arg))
            if param.flags.copy:
                arg = self.clone_arg(arg)
            
            args.append(arg)

        return replace(node, args=args)
