from dataclasses import dataclass
from typing import cast

from antlr4.error.ErrorListener import ErrorListener as ANTLRErrorListener
from antlr4 import InputStream, CommonTokenStream, TerminalNode
from antlr4.Token import CommonToken

from byte.parser.ByteVisitor import ByteVisitor
from byte.parser.ByteParser import ByteParser
from byte.parser.ByteLexer import ByteLexer
from byte import ast


@dataclass
class FuncName:
    identifier: str | None = None
    extend_type: ast.Type | None = None
    op: str | None = None


class ByteErrorListener(ANTLRErrorListener):
    def __init__(self, file: ast.File):
        self.file = file
    
    def syntaxError(self, _, offendingSymbol: CommonToken, line: int, column: int, _msg, _e):
        pos = ast.Position(line, column)
        pos.comptime_error(self.file, f'invalid syntax \'{offendingSymbol.text}\'')

class ByteASTBuilder(ByteVisitor):
    def __init__(self, file: ast.File):
        self.file = file
    
    def pos(self, ctx):
        return ast.Position(ctx.start.line, ctx.start.column)
    
    def build(self):
        lexer = ByteLexer(InputStream(self.file.src))
        parser = ByteParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(ByteErrorListener(self.file))
        return self.visitProgram(parser.program())
    
    def visitProgram(self, ctx):
        return ast.Program(self.pos(ctx), [self.visit(stmt) for stmt in ctx.stmt()])
    
    def visitType(self, ctx):
        if ctx.AMPERSAND():
            return ast.ReferenceType(self.visit(ctx.type_()))
        
        return ast.Type(ctx.getText())
    
    def visitArgs(self, ctx):
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitArg(self, ctx):
        value = self.visit(ctx.expr())
        return ast.Arg(self.pos(ctx), value.type, value)
    
    def visitReturn(self, ctx):
        expr = self.visit(ctx.expr()) if ctx.expr() is not None else None
        return ast.Return(self.pos(ctx), expr.type if expr is not None else self.file.type_map.get('nil'), expr)
    
    def visitBreak(self, ctx):
        return ast.Break(self.pos(ctx))
    
    def visitContinue(self, ctx):
        return ast.Continue(self.pos(ctx))
    
    def visitBody(self, ctx):
        return ast.Body(self.pos(ctx), self.file.type_map.get('any'), [self.visit(stmt) for stmt in ctx.bodyStmts()])
    
    def visitParams(self, ctx):
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParam(self, ctx):
        return ast.Param(
            self.pos(ctx), self.visitType(ctx.type_()), ctx.ID().getText(),
            ctx.MUTABLE() is not None
        )
    
    def visitFuncName(self, ctx):
        extend_type = self.visitType(ctx.extend_type) if ctx.extend_type is not None else None
        identifier = op = None
        if ctx.ID():
            identifier = ctx.ID().getText()
        elif ctx.op:
            op = ctx.op.text
        elif ctx.NEW():
            identifier = 'new'
        
        return FuncName(identifier, extend_type, op)
    
    def visitFuncAssign(self, ctx):
        func_name = self.visitFuncName(ctx.funcName())
        flags = ast.FunctionFlags(static=ctx.STATIC() is not None or func_name.identifier == 'new')
        return ast.Function(
            self.pos(ctx), self.visitType(ctx.return_type) if ctx.return_type is not None else
                self.file.type_map.get('nil'), func_name.identifier or func_name.op,
            self.visitParams(ctx.params()), self.visitBody(ctx.body()),
            flags, func_name.extend_type
        )
    
    def visitVarAssign(self, ctx):
        value = self.visit(ctx.expr())
        return ast.Variable(
            self.pos(ctx), value.type, ctx.ID().getText(), value,
            ctx.MUTABLE() is not None, ctx.op.text if ctx.op is not None else None
        )
    
    def visitIfStmt(self, ctx):
        return ast.If(
            self.pos(ctx), self.visit(ctx.expr()),
            self.visitBody(ctx.body()), self.visitElseStmt(ctx.elseStmt()),
            [self.visitElseifStmt(elseif) for elseif in ctx.elseifStmt()]
        )
    
    def visitElseStmt(self, ctx):
        return self.visitBody(ctx.body()) if ctx is not None else None
    
    def visitElseifStmt(self, ctx):
        return ast.Elseif(self.pos(ctx), self.visit(ctx.expr()), self.visitBody(ctx.body()))
    
    def visitWhileStmt(self, ctx):
        return ast.While(self.pos(ctx), self.visit(ctx.expr()), self.visitBody(ctx.body()))
    
    def visitForRangeStmt(self, ctx):
        return ast.ForRange(
            self.pos(ctx), ctx.ID().getText(), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visitBody(ctx.body()),
            self.visit(ctx.expr(2)) if len(ctx.expr()) == 3 else None
        )
    
    def visitUseStmt(self, ctx):
        return ast.Use(self.pos(ctx), ctx.STRING().getText()[1:-1])
    
    def visitDeferStmt(self, ctx):
        return ast.Defer(self.pos(ctx), self.visit(ctx.expr()))
    
    def visitInt(self, ctx):
        return ast.Int(self.pos(ctx), self.file.type_map.get('int'), int(ctx.getText()))
    
    def visitFloat(self, ctx):
        return ast.Float(self.pos(ctx), self.file.type_map.get('float'), float(ctx.getText()))
    
    def visitString(self, ctx):
        return ast.String(self.pos(ctx), self.file.type_map.get('string'), ctx.getText()[1:-1])
    
    def visitStringPointer(self, ctx):
        return ast.StringPointer(self.pos(ctx), self.file.type_map.get('pointer'), ctx.getText()[1:-1])
    
    def visitBool(self, ctx):
        return ast.Bool(self.pos(ctx), self.file.type_map.get('bool'), ctx.getText() == 'true')
    
    def visitId(self, ctx):
        return ast.Id(self.pos(ctx), self.file.type_map.get('any'), ctx.getText())
    
    def visitCall(self, ctx):
        return ast.Call(
            self.pos(ctx), self.file.type_map.get('any'), ctx.ID().getText(), self.visitArgs(ctx.args())
        )
    
    def visitParen(self, ctx):
        expr = self.visit(ctx.expr())
        return ast.Bracketed(self.pos(ctx), expr.type, expr)
    
    def visitTernary(self, ctx):
        if ctx.ELSE():
            cond = self.visit(ctx.logical(1))
            true = self.visit(ctx.logical(0))
            false = self.visit(ctx.logical(2))
            return ast.Ternary(self.pos(ctx), true.type, cond, true, false)
        
        return self.visit(ctx.logical(0))
    
    def generic_op(self, ctx, operand_list):
        node = self.visit(operand_list[0])
        for i in range(1, len(operand_list)):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(operand_list[i])
            node = ast.Operation(self.pos(ctx), self.file.type_map.get('any'), op, node, right)
        
        return node
    
    def visitLogical(self, ctx):
        return self.generic_op(ctx, ctx.relational())
    
    def visitRelational(self, ctx):
        return self.generic_op(ctx, ctx.addition())
    
    def visitAddition(self, ctx):
        return self.generic_op(ctx, ctx.multiplication())
    
    def visitMultiplication(self, ctx):
        return self.generic_op(ctx, ctx.unary())
    
    def visitUnary(self, ctx):
        if ctx.unary():
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.unary())
            return ast.UnaryOperation(self.pos(ctx), self.file.type_map.get('any'), op, operand)
        
        return self.visit(ctx.postfix())
    
    def visitPostfix(self, ctx):
        node = self.visit(ctx.primary())
        ids = cast(list[TerminalNode], ctx.ID())
        arg_lists = ctx.args()
        arg_index = 0
        for i, id_token in enumerate(ids):
            name = id_token.getText()
            if arg_index < len(arg_lists) and ctx.getChildCount() > 0:
                if ctx.args(arg_index):
                    args = self.visitArgs(ctx.args(arg_index))
                    node = ast.Attribute(self.pos(ctx), self.file.type_map.get('any'), node, name, args)
                    arg_index += 1
                    continue
            
            node = ast.Attribute(self.pos(ctx), self.file.type_map.get('any'), node, name)
        
        return node
    
    def visitAttr(self, ctx):
        return ast.Attribute(
            self.pos(ctx), self.file.type_map.get('any'), self.visit(ctx.expr()), ctx.ID().getText(),
            self.visitArgs(ctx.args()) if ctx.LPAREN() is not None else None
        )
    
    def visitNew(self, ctx):
        return ast.New(
            self.pos(ctx), self.file.type_map.get('any'), self.visitType(ctx.type_()),
            self.visitArgs(ctx.args())
        )
