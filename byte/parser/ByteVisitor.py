# Generated from byte/Byte.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ByteParser import ByteParser
else:
    from ByteParser import ByteParser

# This class defines a complete generic visitor for a parse tree produced by ByteParser.

class ByteVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ByteParser#program.
    def visitProgram(self, ctx:ByteParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#type.
    def visitType(self, ctx:ByteParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#stmt.
    def visitStmt(self, ctx:ByteParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#bodyStmt.
    def visitBodyStmt(self, ctx:ByteParser.BodyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#return.
    def visitReturn(self, ctx:ByteParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#break.
    def visitBreak(self, ctx:ByteParser.BreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#continue.
    def visitContinue(self, ctx:ByteParser.ContinueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#body.
    def visitBody(self, ctx:ByteParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#ifStmt.
    def visitIfStmt(self, ctx:ByteParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#elseifStmt.
    def visitElseifStmt(self, ctx:ByteParser.ElseifStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#elseStmt.
    def visitElseStmt(self, ctx:ByteParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#whileStmt.
    def visitWhileStmt(self, ctx:ByteParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#useStmt.
    def visitUseStmt(self, ctx:ByteParser.UseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#deferStmt.
    def visitDeferStmt(self, ctx:ByteParser.DeferStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#forRangeStmt.
    def visitForRangeStmt(self, ctx:ByteParser.ForRangeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#funcName.
    def visitFuncName(self, ctx:ByteParser.FuncNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#genericParams.
    def visitGenericParams(self, ctx:ByteParser.GenericParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#funcAssign.
    def visitFuncAssign(self, ctx:ByteParser.FuncAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#varAssign.
    def visitVarAssign(self, ctx:ByteParser.VarAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#classAssign.
    def visitClassAssign(self, ctx:ByteParser.ClassAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#classBody.
    def visitClassBody(self, ctx:ByteParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#arg.
    def visitArg(self, ctx:ByteParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#args.
    def visitArgs(self, ctx:ByteParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#param.
    def visitParam(self, ctx:ByteParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#params.
    def visitParams(self, ctx:ByteParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#expr.
    def visitExpr(self, ctx:ByteParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#ternary.
    def visitTernary(self, ctx:ByteParser.TernaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#logical.
    def visitLogical(self, ctx:ByteParser.LogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#relational.
    def visitRelational(self, ctx:ByteParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#addition.
    def visitAddition(self, ctx:ByteParser.AdditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#multiplication.
    def visitMultiplication(self, ctx:ByteParser.MultiplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#unary.
    def visitUnary(self, ctx:ByteParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#postfix.
    def visitPostfix(self, ctx:ByteParser.PostfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#call.
    def visitCall(self, ctx:ByteParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#new.
    def visitNew(self, ctx:ByteParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#paren.
    def visitParen(self, ctx:ByteParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#int.
    def visitInt(self, ctx:ByteParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#float.
    def visitFloat(self, ctx:ByteParser.FloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#string.
    def visitString(self, ctx:ByteParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#stringPointer.
    def visitStringPointer(self, ctx:ByteParser.StringPointerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#bool.
    def visitBool(self, ctx:ByteParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ByteParser#id.
    def visitId(self, ctx:ByteParser.IdContext):
        return self.visitChildren(ctx)



del ByteParser