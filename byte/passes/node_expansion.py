from typing import cast

from byte.passes import ByteCompilerPass
from byte import ast


class NodeExpansion(ByteCompilerPass):
    def visitBody(self, node: ast.Body):
        nodes = []
        has_returned = False
        for stmt in node.nodes:
            if isinstance(stmt, ast.Return):
                nodes.extend(self.scope.data.end_of_scope_nodes)
                self.scope.data.end_of_scope_nodes = []
                has_returned = True
            
            nodes.append(self.visit(stmt))
        
        if not has_returned:
            nodes.extend(self.scope.data.end_of_scope_nodes)
            self.scope.data.end_of_scope_nodes = []
        
        return ast.Body(node.pos, node.type, nodes)
    
    def visitDefer(self, node: ast.Defer):
        self.scope.data.end_of_scope_nodes.append(self.visit(node.expr))
        return ast.Comment(node.pos, str(node))
    
    def visitOperation(self, node: ast.Operation):
        left = self.visit(node.left)
        right = self.visit(node.right)
        callee = f'{node.op}.{left.type}.{right.type}'
        return ast.Call(node.pos, node.type, callee, [left.to_arg(), right.to_arg()])
    
    def visitUnaryOperation(self, node: ast.UnaryOperation):
        value = self.visit(node.value)
        callee = f'{node.op}.{value.type}'
        return ast.Call(node.pos, node.type, callee, [value.to_arg()])
    
    def visitAttribute(self, node: ast.Attribute):
        value = self.visit(node.value)
        callee = f'{value.type}.{node.attr}'
        symbol = self.scope.symbol_table.get(callee)
        func = cast(ast.Function, symbol.value)
        args = [cast(ast.Arg, self.visit(arg)) for arg in node.args or []]
        if not func.flags.static:
            args.append(value.to_arg())
        
        return ast.Call(node.pos, node.type, callee, args)
