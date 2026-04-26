from enum import Enum, auto

from byte.passes import ByteCompilerPass
from byte import ast


class ReturnStatus(Enum):
    NEVER = auto()
    SOMETIMES = auto()
    ALWAYS = auto()

class ReturnChecker(ByteCompilerPass):
    def visitBody(self, node: ast.Body):
        for stmt in node.nodes:
            status = self.visit(stmt)
            if status == ReturnStatus.ALWAYS:
                return ReturnStatus.ALWAYS
            
            if status == ReturnStatus.SOMETIMES:
                return ReturnStatus.SOMETIMES
        
        return ReturnStatus.NEVER
    
    def visitReturn(self, _):
        return ReturnStatus.ALWAYS
    
    def visitIf(self, node: ast.If):
        then_status = self.visit(node.body)
        if node.else_body is not None:
            else_status = self.visit(node.else_body)
        else:
            else_status = ReturnStatus.NEVER
        
        if then_status == ReturnStatus.ALWAYS and else_status == ReturnStatus.ALWAYS:
            return ReturnStatus.ALWAYS
        
        if then_status == ReturnStatus.NEVER and else_status == ReturnStatus.NEVER:
            return ReturnStatus.NEVER
        
        return ReturnStatus.SOMETIMES
    
    def visitWhile(self, _):
        return ReturnStatus.NEVER
    
    def visitForRange(self, _):
        return ReturnStatus.NEVER
    
    def visitFunction(self, node: ast.Function):
        if node.body is None:
            return node
        
        status = self.visit(node.body)
        if str(node.ret_type) != 'nil' and status != ReturnStatus.ALWAYS:
            node.pos.comptime_error(self.file, 'expected all code paths to return a value')
        
        return node
