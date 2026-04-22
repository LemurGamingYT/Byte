# Generated from byte/Byte.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,45,278,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        1,0,5,0,56,8,0,10,0,12,0,59,9,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,1,2,
        1,2,1,2,3,2,71,8,2,1,3,1,3,1,3,3,3,76,8,3,1,3,1,3,3,3,80,8,3,1,4,
        1,4,5,4,84,8,4,10,4,12,4,87,9,4,1,4,1,4,1,5,1,5,1,5,1,5,5,5,95,8,
        5,10,5,12,5,98,9,5,1,5,3,5,101,8,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,
        7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,3,11,
        124,8,11,1,11,1,11,1,11,1,11,1,11,3,11,131,8,11,1,11,3,11,134,8,
        11,1,12,3,12,137,8,12,1,12,1,12,1,12,1,12,3,12,143,8,12,1,12,1,12,
        1,12,3,12,148,8,12,1,12,1,12,1,13,1,13,3,13,154,8,13,1,13,1,13,1,
        13,3,13,159,8,13,1,13,1,13,1,13,3,13,164,8,13,1,14,1,14,1,15,1,15,
        1,15,5,15,171,8,15,10,15,12,15,174,9,15,1,16,3,16,177,8,16,1,16,
        1,16,1,16,1,17,1,17,1,17,5,17,185,8,17,10,17,12,17,188,9,17,1,18,
        1,18,1,19,1,19,1,19,1,19,1,19,1,19,3,19,198,8,19,1,20,1,20,1,20,
        5,20,203,8,20,10,20,12,20,206,9,20,1,21,1,21,1,21,5,21,211,8,21,
        10,21,12,21,214,9,21,1,22,1,22,1,22,5,22,219,8,22,10,22,12,22,222,
        9,22,1,23,1,23,1,23,5,23,227,8,23,10,23,12,23,230,9,23,1,24,1,24,
        1,24,3,24,235,8,24,1,25,1,25,1,25,1,25,1,25,3,25,242,8,25,1,25,3,
        25,245,8,25,5,25,247,8,25,10,25,12,25,250,9,25,1,26,1,26,1,26,3,
        26,255,8,26,1,26,1,26,1,26,1,26,1,26,3,26,262,8,26,1,26,1,26,1,26,
        1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,3,26,276,8,26,1,26,
        0,0,27,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,
        42,44,46,48,50,52,0,7,1,0,20,33,1,0,20,24,1,0,31,32,1,0,25,30,1,
        0,20,21,1,0,22,24,2,0,20,21,33,33,295,0,57,1,0,0,0,2,62,1,0,0,0,
        4,70,1,0,0,0,6,79,1,0,0,0,8,81,1,0,0,0,10,90,1,0,0,0,12,102,1,0,
        0,0,14,107,1,0,0,0,16,110,1,0,0,0,18,114,1,0,0,0,20,117,1,0,0,0,
        22,133,1,0,0,0,24,136,1,0,0,0,26,163,1,0,0,0,28,165,1,0,0,0,30,167,
        1,0,0,0,32,176,1,0,0,0,34,181,1,0,0,0,36,189,1,0,0,0,38,191,1,0,
        0,0,40,199,1,0,0,0,42,207,1,0,0,0,44,215,1,0,0,0,46,223,1,0,0,0,
        48,234,1,0,0,0,50,236,1,0,0,0,52,275,1,0,0,0,54,56,3,4,2,0,55,54,
        1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,60,1,0,0,0,
        59,57,1,0,0,0,60,61,5,0,0,1,61,1,1,0,0,0,62,63,5,19,0,0,63,3,1,0,
        0,0,64,71,3,26,13,0,65,71,3,24,12,0,66,71,3,16,8,0,67,71,3,10,5,
        0,68,71,3,18,9,0,69,71,3,36,18,0,70,64,1,0,0,0,70,65,1,0,0,0,70,
        66,1,0,0,0,70,67,1,0,0,0,70,68,1,0,0,0,70,69,1,0,0,0,71,5,1,0,0,
        0,72,80,3,4,2,0,73,75,5,8,0,0,74,76,3,36,18,0,75,74,1,0,0,0,75,76,
        1,0,0,0,76,80,1,0,0,0,77,80,5,11,0,0,78,80,5,12,0,0,79,72,1,0,0,
        0,79,73,1,0,0,0,79,77,1,0,0,0,79,78,1,0,0,0,80,7,1,0,0,0,81,85,5,
        39,0,0,82,84,3,6,3,0,83,82,1,0,0,0,84,87,1,0,0,0,85,83,1,0,0,0,85,
        86,1,0,0,0,86,88,1,0,0,0,87,85,1,0,0,0,88,89,5,40,0,0,89,9,1,0,0,
        0,90,91,5,1,0,0,91,92,3,36,18,0,92,96,3,8,4,0,93,95,3,12,6,0,94,
        93,1,0,0,0,95,98,1,0,0,0,96,94,1,0,0,0,96,97,1,0,0,0,97,100,1,0,
        0,0,98,96,1,0,0,0,99,101,3,14,7,0,100,99,1,0,0,0,100,101,1,0,0,0,
        101,11,1,0,0,0,102,103,5,5,0,0,103,104,5,1,0,0,104,105,3,36,18,0,
        105,106,3,8,4,0,106,13,1,0,0,0,107,108,5,5,0,0,108,109,3,8,4,0,109,
        15,1,0,0,0,110,111,5,10,0,0,111,112,3,36,18,0,112,113,3,8,4,0,113,
        17,1,0,0,0,114,115,5,3,0,0,115,116,5,16,0,0,116,19,1,0,0,0,117,118,
        5,7,0,0,118,119,3,36,18,0,119,21,1,0,0,0,120,121,3,2,1,0,121,122,
        5,34,0,0,122,124,1,0,0,0,123,120,1,0,0,0,123,124,1,0,0,0,124,125,
        1,0,0,0,125,134,5,19,0,0,126,134,7,0,0,0,127,128,3,2,1,0,128,129,
        5,34,0,0,129,131,1,0,0,0,130,127,1,0,0,0,130,131,1,0,0,0,131,132,
        1,0,0,0,132,134,5,2,0,0,133,123,1,0,0,0,133,126,1,0,0,0,133,130,
        1,0,0,0,134,23,1,0,0,0,135,137,5,9,0,0,136,135,1,0,0,0,136,137,1,
        0,0,0,137,138,1,0,0,0,138,139,5,4,0,0,139,140,3,22,11,0,140,142,
        5,37,0,0,141,143,3,34,17,0,142,141,1,0,0,0,142,143,1,0,0,0,143,144,
        1,0,0,0,144,147,5,38,0,0,145,146,5,41,0,0,146,148,3,2,1,0,147,145,
        1,0,0,0,147,148,1,0,0,0,148,149,1,0,0,0,149,150,3,8,4,0,150,25,1,
        0,0,0,151,153,5,19,0,0,152,154,7,1,0,0,153,152,1,0,0,0,153,154,1,
        0,0,0,154,155,1,0,0,0,155,156,5,36,0,0,156,164,3,36,18,0,157,159,
        5,6,0,0,158,157,1,0,0,0,158,159,1,0,0,0,159,160,1,0,0,0,160,161,
        5,19,0,0,161,162,5,36,0,0,162,164,3,36,18,0,163,151,1,0,0,0,163,
        158,1,0,0,0,164,27,1,0,0,0,165,166,3,36,18,0,166,29,1,0,0,0,167,
        172,3,28,14,0,168,169,5,35,0,0,169,171,3,28,14,0,170,168,1,0,0,0,
        171,174,1,0,0,0,172,170,1,0,0,0,172,173,1,0,0,0,173,31,1,0,0,0,174,
        172,1,0,0,0,175,177,5,6,0,0,176,175,1,0,0,0,176,177,1,0,0,0,177,
        178,1,0,0,0,178,179,3,2,1,0,179,180,5,19,0,0,180,33,1,0,0,0,181,
        186,3,32,16,0,182,183,5,35,0,0,183,185,3,32,16,0,184,182,1,0,0,0,
        185,188,1,0,0,0,186,184,1,0,0,0,186,187,1,0,0,0,187,35,1,0,0,0,188,
        186,1,0,0,0,189,190,3,38,19,0,190,37,1,0,0,0,191,197,3,40,20,0,192,
        193,5,1,0,0,193,194,3,40,20,0,194,195,5,5,0,0,195,196,3,40,20,0,
        196,198,1,0,0,0,197,192,1,0,0,0,197,198,1,0,0,0,198,39,1,0,0,0,199,
        204,3,42,21,0,200,201,7,2,0,0,201,203,3,42,21,0,202,200,1,0,0,0,
        203,206,1,0,0,0,204,202,1,0,0,0,204,205,1,0,0,0,205,41,1,0,0,0,206,
        204,1,0,0,0,207,212,3,44,22,0,208,209,7,3,0,0,209,211,3,44,22,0,
        210,208,1,0,0,0,211,214,1,0,0,0,212,210,1,0,0,0,212,213,1,0,0,0,
        213,43,1,0,0,0,214,212,1,0,0,0,215,220,3,46,23,0,216,217,7,4,0,0,
        217,219,3,46,23,0,218,216,1,0,0,0,219,222,1,0,0,0,220,218,1,0,0,
        0,220,221,1,0,0,0,221,45,1,0,0,0,222,220,1,0,0,0,223,228,3,48,24,
        0,224,225,7,5,0,0,225,227,3,48,24,0,226,224,1,0,0,0,227,230,1,0,
        0,0,228,226,1,0,0,0,228,229,1,0,0,0,229,47,1,0,0,0,230,228,1,0,0,
        0,231,232,7,6,0,0,232,235,3,48,24,0,233,235,3,50,25,0,234,231,1,
        0,0,0,234,233,1,0,0,0,235,49,1,0,0,0,236,248,3,52,26,0,237,238,5,
        34,0,0,238,244,5,19,0,0,239,241,5,37,0,0,240,242,3,30,15,0,241,240,
        1,0,0,0,241,242,1,0,0,0,242,243,1,0,0,0,243,245,5,38,0,0,244,239,
        1,0,0,0,244,245,1,0,0,0,245,247,1,0,0,0,246,237,1,0,0,0,247,250,
        1,0,0,0,248,246,1,0,0,0,248,249,1,0,0,0,249,51,1,0,0,0,250,248,1,
        0,0,0,251,252,5,19,0,0,252,254,5,37,0,0,253,255,3,30,15,0,254,253,
        1,0,0,0,254,255,1,0,0,0,255,256,1,0,0,0,256,276,5,38,0,0,257,258,
        5,2,0,0,258,259,3,2,1,0,259,261,5,37,0,0,260,262,3,30,15,0,261,260,
        1,0,0,0,261,262,1,0,0,0,262,263,1,0,0,0,263,264,5,38,0,0,264,276,
        1,0,0,0,265,266,5,37,0,0,266,267,3,36,18,0,267,268,5,38,0,0,268,
        276,1,0,0,0,269,276,5,14,0,0,270,276,5,15,0,0,271,276,5,16,0,0,272,
        276,5,17,0,0,273,276,5,18,0,0,274,276,5,19,0,0,275,251,1,0,0,0,275,
        257,1,0,0,0,275,265,1,0,0,0,275,269,1,0,0,0,275,270,1,0,0,0,275,
        271,1,0,0,0,275,272,1,0,0,0,275,273,1,0,0,0,275,274,1,0,0,0,276,
        53,1,0,0,0,31,57,70,75,79,85,96,100,123,130,133,136,142,147,153,
        158,163,172,176,186,197,204,212,220,228,234,241,244,248,254,261,
        275
    ]

class ByteParser ( Parser ):

    grammarFileName = "Byte.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'new'", "'use'", "'fn'", "'else'", 
                     "'mut'", "'defer'", "'return'", "'static'", "'while'", 
                     "'break'", "'continue'", "'''", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'+'", "'-'", "'*'", "'/'", "'%'", "'=='", "'!='", 
                     "'>'", "'<'", "'>='", "'<='", "'&&'", "'||'", "'!'", 
                     "'.'", "','", "'='", "'('", "')'", "'{'", "'}'", "'->'" ]

    symbolicNames = [ "<INVALID>", "IF", "NEW", "USE", "FUNC", "ELSE", "MUTABLE", 
                      "DEFER", "RETURN", "STATIC", "WHILE", "BREAK", "CONTINUE", 
                      "APOSTROPHE", "INT", "FLOAT", "STRING", "STRING_POINTER", 
                      "BOOL", "ID", "ADD", "SUB", "MUL", "DIV", "MOD", "EEQ", 
                      "NEQ", "GT", "LT", "GTE", "LTE", "AND", "OR", "NOT", 
                      "DOT", "COMMA", "ASSIGN", "LPAREN", "RPAREN", "LBRACE", 
                      "RBRACE", "RETURNS", "COMMENT", "MULTILINE_COMMENT", 
                      "WHITESPACE", "OTHER" ]

    RULE_program = 0
    RULE_type = 1
    RULE_stmt = 2
    RULE_bodyStmts = 3
    RULE_body = 4
    RULE_ifStmt = 5
    RULE_elseifStmt = 6
    RULE_elseStmt = 7
    RULE_whileStmt = 8
    RULE_useStmt = 9
    RULE_deferStmt = 10
    RULE_funcName = 11
    RULE_funcAssign = 12
    RULE_varAssign = 13
    RULE_arg = 14
    RULE_args = 15
    RULE_param = 16
    RULE_params = 17
    RULE_expr = 18
    RULE_ternary = 19
    RULE_logical = 20
    RULE_relational = 21
    RULE_addition = 22
    RULE_multiplication = 23
    RULE_unary = 24
    RULE_postfix = 25
    RULE_primary = 26

    ruleNames =  [ "program", "type", "stmt", "bodyStmts", "body", "ifStmt", 
                   "elseifStmt", "elseStmt", "whileStmt", "useStmt", "deferStmt", 
                   "funcName", "funcAssign", "varAssign", "arg", "args", 
                   "param", "params", "expr", "ternary", "logical", "relational", 
                   "addition", "multiplication", "unary", "postfix", "primary" ]

    EOF = Token.EOF
    IF=1
    NEW=2
    USE=3
    FUNC=4
    ELSE=5
    MUTABLE=6
    DEFER=7
    RETURN=8
    STATIC=9
    WHILE=10
    BREAK=11
    CONTINUE=12
    APOSTROPHE=13
    INT=14
    FLOAT=15
    STRING=16
    STRING_POINTER=17
    BOOL=18
    ID=19
    ADD=20
    SUB=21
    MUL=22
    DIV=23
    MOD=24
    EEQ=25
    NEQ=26
    GT=27
    LT=28
    GTE=29
    LTE=30
    AND=31
    OR=32
    NOT=33
    DOT=34
    COMMA=35
    ASSIGN=36
    LPAREN=37
    RPAREN=38
    LBRACE=39
    RBRACE=40
    RETURNS=41
    COMMENT=42
    MULTILINE_COMMENT=43
    WHITESPACE=44
    OTHER=45

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ByteParser.EOF, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.StmtContext)
            else:
                return self.getTypedRuleContext(ByteParser.StmtContext,i)


        def getRuleIndex(self):
            return ByteParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = ByteParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033067614) != 0):
                self.state = 54
                self.stmt()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 60
            self.match(ByteParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ByteParser.ID, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = ByteParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(ByteParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varAssign(self):
            return self.getTypedRuleContext(ByteParser.VarAssignContext,0)


        def funcAssign(self):
            return self.getTypedRuleContext(ByteParser.FuncAssignContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(ByteParser.WhileStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(ByteParser.IfStmtContext,0)


        def useStmt(self):
            return self.getTypedRuleContext(ByteParser.UseStmtContext,0)


        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = ByteParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 65
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 66
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 67
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 68
                self.useStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 69
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyStmtsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ByteParser.RULE_bodyStmts

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BreakContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BREAK(self):
            return self.getToken(ByteParser.BREAK, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak" ):
                return visitor.visitBreak(self)
            else:
                return visitor.visitChildren(self)


    class BodyStmtContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmt(self):
            return self.getTypedRuleContext(ByteParser.StmtContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBodyStmt" ):
                return visitor.visitBodyStmt(self)
            else:
                return visitor.visitChildren(self)


    class ContinueContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CONTINUE(self):
            return self.getToken(ByteParser.CONTINUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue" ):
                return visitor.visitContinue(self)
            else:
                return visitor.visitChildren(self)


    class ReturnContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RETURN(self):
            return self.getToken(ByteParser.RETURN, 0)
        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn" ):
                return visitor.visitReturn(self)
            else:
                return visitor.visitChildren(self)



    def bodyStmts(self):

        localctx = ByteParser.BodyStmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_bodyStmts)
        try:
            self.state = 79
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 6, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21, 33, 37]:
                localctx = ByteParser.BodyStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 72
                self.stmt()
                pass
            elif token in [8]:
                localctx = ByteParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 73
                self.match(ByteParser.RETURN)
                self.state = 75
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 74
                    self.expr()


                pass
            elif token in [11]:
                localctx = ByteParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 77
                self.match(ByteParser.BREAK)
                pass
            elif token in [12]:
                localctx = ByteParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 78
                self.match(ByteParser.CONTINUE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(ByteParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(ByteParser.RBRACE, 0)

        def bodyStmts(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.BodyStmtsContext)
            else:
                return self.getTypedRuleContext(ByteParser.BodyStmtsContext,i)


        def getRuleIndex(self):
            return ByteParser.RULE_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = ByteParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(ByteParser.LBRACE)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033074014) != 0):
                self.state = 82
                self.bodyStmts()
                self.state = 87
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 88
            self.match(ByteParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(ByteParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(ByteParser.BodyContext,0)


        def elseifStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.ElseifStmtContext)
            else:
                return self.getTypedRuleContext(ByteParser.ElseifStmtContext,i)


        def elseStmt(self):
            return self.getTypedRuleContext(ByteParser.ElseStmtContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = ByteParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(ByteParser.IF)
            self.state = 91
            self.expr()
            self.state = 92
            self.body()
            self.state = 96
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 93
                    self.elseifStmt() 
                self.state = 98
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 99
                self.elseStmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseifStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(ByteParser.ELSE, 0)

        def IF(self):
            return self.getToken(ByteParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(ByteParser.BodyContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_elseifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseifStmt" ):
                return visitor.visitElseifStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseifStmt(self):

        localctx = ByteParser.ElseifStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_elseifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(ByteParser.ELSE)
            self.state = 103
            self.match(ByteParser.IF)
            self.state = 104
            self.expr()
            self.state = 105
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(ByteParser.ELSE, 0)

        def body(self):
            return self.getTypedRuleContext(ByteParser.BodyContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_elseStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseStmt" ):
                return visitor.visitElseStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseStmt(self):

        localctx = ByteParser.ElseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_elseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(ByteParser.ELSE)
            self.state = 108
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(ByteParser.WHILE, 0)

        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(ByteParser.BodyContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = ByteParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.match(ByteParser.WHILE)
            self.state = 111
            self.expr()
            self.state = 112
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USE(self):
            return self.getToken(ByteParser.USE, 0)

        def STRING(self):
            return self.getToken(ByteParser.STRING, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_useStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUseStmt" ):
                return visitor.visitUseStmt(self)
            else:
                return visitor.visitChildren(self)




    def useStmt(self):

        localctx = ByteParser.UseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_useStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.match(ByteParser.USE)
            self.state = 115
            self.match(ByteParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeferStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEFER(self):
            return self.getToken(ByteParser.DEFER, 0)

        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_deferStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeferStmt" ):
                return visitor.visitDeferStmt(self)
            else:
                return visitor.visitChildren(self)




    def deferStmt(self):

        localctx = ByteParser.DeferStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_deferStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.match(ByteParser.DEFER)
            self.state = 118
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.extend_type = None # TypeContext
            self.op = None # Token

        def ID(self):
            return self.getToken(ByteParser.ID, 0)

        def DOT(self):
            return self.getToken(ByteParser.DOT, 0)

        def type_(self):
            return self.getTypedRuleContext(ByteParser.TypeContext,0)


        def ADD(self):
            return self.getToken(ByteParser.ADD, 0)

        def SUB(self):
            return self.getToken(ByteParser.SUB, 0)

        def MUL(self):
            return self.getToken(ByteParser.MUL, 0)

        def DIV(self):
            return self.getToken(ByteParser.DIV, 0)

        def MOD(self):
            return self.getToken(ByteParser.MOD, 0)

        def EEQ(self):
            return self.getToken(ByteParser.EEQ, 0)

        def NEQ(self):
            return self.getToken(ByteParser.NEQ, 0)

        def GT(self):
            return self.getToken(ByteParser.GT, 0)

        def LT(self):
            return self.getToken(ByteParser.LT, 0)

        def GTE(self):
            return self.getToken(ByteParser.GTE, 0)

        def LTE(self):
            return self.getToken(ByteParser.LTE, 0)

        def AND(self):
            return self.getToken(ByteParser.AND, 0)

        def OR(self):
            return self.getToken(ByteParser.OR, 0)

        def NOT(self):
            return self.getToken(ByteParser.NOT, 0)

        def NEW(self):
            return self.getToken(ByteParser.NEW, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_funcName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncName" ):
                return visitor.visitFuncName(self)
            else:
                return visitor.visitChildren(self)




    def funcName(self):

        localctx = ByteParser.FuncNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_funcName)
        self._la = 0 # Token type
        try:
            self.state = 133
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 123
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                if la_ == 1:
                    self.state = 120
                    localctx.extend_type = self.type_()
                    self.state = 121
                    self.match(ByteParser.DOT)


                self.state = 125
                self.match(ByteParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 126
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 17178820608) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 130
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==19:
                    self.state = 127
                    localctx.extend_type = self.type_()
                    self.state = 128
                    self.match(ByteParser.DOT)


                self.state = 132
                self.match(ByteParser.NEW)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.return_type = None # TypeContext

        def FUNC(self):
            return self.getToken(ByteParser.FUNC, 0)

        def funcName(self):
            return self.getTypedRuleContext(ByteParser.FuncNameContext,0)


        def LPAREN(self):
            return self.getToken(ByteParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(ByteParser.RPAREN, 0)

        def body(self):
            return self.getTypedRuleContext(ByteParser.BodyContext,0)


        def STATIC(self):
            return self.getToken(ByteParser.STATIC, 0)

        def params(self):
            return self.getTypedRuleContext(ByteParser.ParamsContext,0)


        def RETURNS(self):
            return self.getToken(ByteParser.RETURNS, 0)

        def type_(self):
            return self.getTypedRuleContext(ByteParser.TypeContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_funcAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncAssign" ):
                return visitor.visitFuncAssign(self)
            else:
                return visitor.visitChildren(self)




    def funcAssign(self):

        localctx = ByteParser.FuncAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 135
                self.match(ByteParser.STATIC)


            self.state = 138
            self.match(ByteParser.FUNC)
            self.state = 139
            self.funcName()
            self.state = 140
            self.match(ByteParser.LPAREN)
            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6 or _la==19:
                self.state = 141
                self.params()


            self.state = 144
            self.match(ByteParser.RPAREN)
            self.state = 147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 145
                self.match(ByteParser.RETURNS)
                self.state = 146
                localctx.return_type = self.type_()


            self.state = 149
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def ID(self):
            return self.getToken(ByteParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(ByteParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def ADD(self):
            return self.getToken(ByteParser.ADD, 0)

        def SUB(self):
            return self.getToken(ByteParser.SUB, 0)

        def MUL(self):
            return self.getToken(ByteParser.MUL, 0)

        def DIV(self):
            return self.getToken(ByteParser.DIV, 0)

        def MOD(self):
            return self.getToken(ByteParser.MOD, 0)

        def MUTABLE(self):
            return self.getToken(ByteParser.MUTABLE, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_varAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarAssign" ):
                return visitor.visitVarAssign(self)
            else:
                return visitor.visitChildren(self)




    def varAssign(self):

        localctx = ByteParser.VarAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.state = 163
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 151
                self.match(ByteParser.ID)
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32505856) != 0):
                    self.state = 152
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 32505856) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 155
                self.match(ByteParser.ASSIGN)
                self.state = 156
                self.expr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 158
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 157
                    self.match(ByteParser.MUTABLE)


                self.state = 160
                self.match(ByteParser.ID)
                self.state = 161
                self.match(ByteParser.ASSIGN)
                self.state = 162
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = ByteParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.ArgContext)
            else:
                return self.getTypedRuleContext(ByteParser.ArgContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.COMMA)
            else:
                return self.getToken(ByteParser.COMMA, i)

        def getRuleIndex(self):
            return ByteParser.RULE_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgs" ):
                return visitor.visitArgs(self)
            else:
                return visitor.visitChildren(self)




    def args(self):

        localctx = ByteParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            self.arg()
            self.state = 172
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 168
                self.match(ByteParser.COMMA)
                self.state = 169
                self.arg()
                self.state = 174
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(ByteParser.TypeContext,0)


        def ID(self):
            return self.getToken(ByteParser.ID, 0)

        def MUTABLE(self):
            return self.getToken(ByteParser.MUTABLE, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = ByteParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 175
                self.match(ByteParser.MUTABLE)


            self.state = 178
            self.type_()
            self.state = 179
            self.match(ByteParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.ParamContext)
            else:
                return self.getTypedRuleContext(ByteParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.COMMA)
            else:
                return self.getToken(ByteParser.COMMA, i)

        def getRuleIndex(self):
            return ByteParser.RULE_params

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParams" ):
                return visitor.visitParams(self)
            else:
                return visitor.visitChildren(self)




    def params(self):

        localctx = ByteParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
            self.param()
            self.state = 186
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 182
                self.match(ByteParser.COMMA)
                self.state = 183
                self.param()
                self.state = 188
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ternary(self):
            return self.getTypedRuleContext(ByteParser.TernaryContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = ByteParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.ternary()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TernaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logical(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.LogicalContext)
            else:
                return self.getTypedRuleContext(ByteParser.LogicalContext,i)


        def IF(self):
            return self.getToken(ByteParser.IF, 0)

        def ELSE(self):
            return self.getToken(ByteParser.ELSE, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_ternary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTernary" ):
                return visitor.visitTernary(self)
            else:
                return visitor.visitChildren(self)




    def ternary(self):

        localctx = ByteParser.TernaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_ternary)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            self.logical()
            self.state = 197
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.state = 192
                self.match(ByteParser.IF)
                self.state = 193
                self.logical()
                self.state = 194
                self.match(ByteParser.ELSE)
                self.state = 195
                self.logical()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relational(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.RelationalContext)
            else:
                return self.getTypedRuleContext(ByteParser.RelationalContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.AND)
            else:
                return self.getToken(ByteParser.AND, i)

        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.OR)
            else:
                return self.getToken(ByteParser.OR, i)

        def getRuleIndex(self):
            return ByteParser.RULE_logical

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical" ):
                return visitor.visitLogical(self)
            else:
                return visitor.visitChildren(self)




    def logical(self):

        localctx = ByteParser.LogicalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_logical)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.relational()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31 or _la==32:
                self.state = 200
                _la = self._input.LA(1)
                if not(_la==31 or _la==32):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 201
                self.relational()
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.AdditionContext)
            else:
                return self.getTypedRuleContext(ByteParser.AdditionContext,i)


        def EEQ(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.EEQ)
            else:
                return self.getToken(ByteParser.EEQ, i)

        def NEQ(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.NEQ)
            else:
                return self.getToken(ByteParser.NEQ, i)

        def GT(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.GT)
            else:
                return self.getToken(ByteParser.GT, i)

        def LT(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.LT)
            else:
                return self.getToken(ByteParser.LT, i)

        def GTE(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.GTE)
            else:
                return self.getToken(ByteParser.GTE, i)

        def LTE(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.LTE)
            else:
                return self.getToken(ByteParser.LTE, i)

        def getRuleIndex(self):
            return ByteParser.RULE_relational

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelational" ):
                return visitor.visitRelational(self)
            else:
                return visitor.visitChildren(self)




    def relational(self):

        localctx = ByteParser.RelationalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_relational)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.addition()
            self.state = 212
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2113929216) != 0):
                self.state = 208
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2113929216) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 209
                self.addition()
                self.state = 214
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplication(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.MultiplicationContext)
            else:
                return self.getTypedRuleContext(ByteParser.MultiplicationContext,i)


        def ADD(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.ADD)
            else:
                return self.getToken(ByteParser.ADD, i)

        def SUB(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.SUB)
            else:
                return self.getToken(ByteParser.SUB, i)

        def getRuleIndex(self):
            return ByteParser.RULE_addition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddition" ):
                return visitor.visitAddition(self)
            else:
                return visitor.visitChildren(self)




    def addition(self):

        localctx = ByteParser.AdditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_addition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.multiplication()
            self.state = 220
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,22,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 216
                    _la = self._input.LA(1)
                    if not(_la==20 or _la==21):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 217
                    self.multiplication() 
                self.state = 222
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,22,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unary(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.UnaryContext)
            else:
                return self.getTypedRuleContext(ByteParser.UnaryContext,i)


        def MUL(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.MUL)
            else:
                return self.getToken(ByteParser.MUL, i)

        def DIV(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.DIV)
            else:
                return self.getToken(ByteParser.DIV, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.MOD)
            else:
                return self.getToken(ByteParser.MOD, i)

        def getRuleIndex(self):
            return ByteParser.RULE_multiplication

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplication" ):
                return visitor.visitMultiplication(self)
            else:
                return visitor.visitChildren(self)




    def multiplication(self):

        localctx = ByteParser.MultiplicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_multiplication)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 223
            self.unary()
            self.state = 228
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 29360128) != 0):
                self.state = 224
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 29360128) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 225
                self.unary()
                self.state = 230
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unary(self):
            return self.getTypedRuleContext(ByteParser.UnaryContext,0)


        def NOT(self):
            return self.getToken(ByteParser.NOT, 0)

        def ADD(self):
            return self.getToken(ByteParser.ADD, 0)

        def SUB(self):
            return self.getToken(ByteParser.SUB, 0)

        def postfix(self):
            return self.getTypedRuleContext(ByteParser.PostfixContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_unary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary" ):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)




    def unary(self):

        localctx = ByteParser.UnaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_unary)
        self._la = 0 # Token type
        try:
            self.state = 234
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20, 21, 33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 231
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8593080320) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 232
                self.unary()
                pass
            elif token in [2, 14, 15, 16, 17, 18, 19, 37]:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self.postfix()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(ByteParser.PrimaryContext,0)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.DOT)
            else:
                return self.getToken(ByteParser.DOT, i)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.ID)
            else:
                return self.getToken(ByteParser.ID, i)

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.LPAREN)
            else:
                return self.getToken(ByteParser.LPAREN, i)

        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.RPAREN)
            else:
                return self.getToken(ByteParser.RPAREN, i)

        def args(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.ArgsContext)
            else:
                return self.getTypedRuleContext(ByteParser.ArgsContext,i)


        def getRuleIndex(self):
            return ByteParser.RULE_postfix

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfix" ):
                return visitor.visitPostfix(self)
            else:
                return visitor.visitChildren(self)




    def postfix(self):

        localctx = ByteParser.PostfixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_postfix)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self.primary()
            self.state = 248
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 237
                self.match(ByteParser.DOT)
                self.state = 238
                self.match(ByteParser.ID)
                self.state = 244
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
                if la_ == 1:
                    self.state = 239
                    self.match(ByteParser.LPAREN)
                    self.state = 241
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033065988) != 0):
                        self.state = 240
                        self.args()


                    self.state = 243
                    self.match(ByteParser.RPAREN)


                self.state = 250
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ByteParser.RULE_primary

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CallContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(ByteParser.ID, 0)
        def LPAREN(self):
            return self.getToken(ByteParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(ByteParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(ByteParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)


    class NewContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEW(self):
            return self.getToken(ByteParser.NEW, 0)
        def type_(self):
            return self.getTypedRuleContext(ByteParser.TypeContext,0)

        def LPAREN(self):
            return self.getToken(ByteParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(ByteParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(ByteParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNew" ):
                return visitor.visitNew(self)
            else:
                return visitor.visitChildren(self)


    class ParenContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(ByteParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(ByteParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(ByteParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParen" ):
                return visitor.visitParen(self)
            else:
                return visitor.visitChildren(self)


    class StringContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(ByteParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)


    class BoolContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOL(self):
            return self.getToken(ByteParser.BOOL, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBool" ):
                return visitor.visitBool(self)
            else:
                return visitor.visitChildren(self)


    class StringPointerContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING_POINTER(self):
            return self.getToken(ByteParser.STRING_POINTER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringPointer" ):
                return visitor.visitStringPointer(self)
            else:
                return visitor.visitChildren(self)


    class IdContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(ByteParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitId" ):
                return visitor.visitId(self)
            else:
                return visitor.visitChildren(self)


    class FloatContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(ByteParser.FLOAT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat" ):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)


    class IntContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ByteParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(ByteParser.INT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInt" ):
                return visitor.visitInt(self)
            else:
                return visitor.visitChildren(self)



    def primary(self):

        localctx = ByteParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_primary)
        self._la = 0 # Token type
        try:
            self.state = 275
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                localctx = ByteParser.CallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 251
                self.match(ByteParser.ID)
                self.state = 252
                self.match(ByteParser.LPAREN)
                self.state = 254
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033065988) != 0):
                    self.state = 253
                    self.args()


                self.state = 256
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = ByteParser.NewContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 257
                self.match(ByteParser.NEW)
                self.state = 258
                self.type_()
                self.state = 259
                self.match(ByteParser.LPAREN)
                self.state = 261
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033065988) != 0):
                    self.state = 260
                    self.args()


                self.state = 263
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = ByteParser.ParenContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 265
                self.match(ByteParser.LPAREN)
                self.state = 266
                self.expr()
                self.state = 267
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = ByteParser.IntContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 269
                self.match(ByteParser.INT)
                pass

            elif la_ == 5:
                localctx = ByteParser.FloatContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 270
                self.match(ByteParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = ByteParser.StringContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 271
                self.match(ByteParser.STRING)
                pass

            elif la_ == 7:
                localctx = ByteParser.StringPointerContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 272
                self.match(ByteParser.STRING_POINTER)
                pass

            elif la_ == 8:
                localctx = ByteParser.BoolContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 273
                self.match(ByteParser.BOOL)
                pass

            elif la_ == 9:
                localctx = ByteParser.IdContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 274
                self.match(ByteParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





