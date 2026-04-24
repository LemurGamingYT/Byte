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
        4,1,46,286,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        1,0,5,0,56,8,0,10,0,12,0,59,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,5,1,
        68,8,1,10,1,12,1,71,9,1,1,2,1,2,1,2,1,2,1,2,1,2,3,2,79,8,2,1,3,1,
        3,1,3,3,3,84,8,3,1,3,1,3,3,3,88,8,3,1,4,1,4,5,4,92,8,4,10,4,12,4,
        95,9,4,1,4,1,4,1,5,1,5,1,5,1,5,5,5,103,8,5,10,5,12,5,106,9,5,1,5,
        3,5,109,8,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,9,
        1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,3,11,132,8,11,1,11,1,11,1,
        11,1,11,1,11,3,11,139,8,11,1,11,3,11,142,8,11,1,12,3,12,145,8,12,
        1,12,1,12,1,12,1,12,3,12,151,8,12,1,12,1,12,1,12,3,12,156,8,12,1,
        12,1,12,1,13,1,13,3,13,162,8,13,1,13,1,13,1,13,3,13,167,8,13,1,13,
        1,13,1,13,3,13,172,8,13,1,14,1,14,1,15,1,15,1,15,5,15,179,8,15,10,
        15,12,15,182,9,15,1,16,3,16,185,8,16,1,16,1,16,1,16,1,17,1,17,1,
        17,5,17,193,8,17,10,17,12,17,196,9,17,1,18,1,18,1,19,1,19,1,19,1,
        19,1,19,1,19,3,19,206,8,19,1,20,1,20,1,20,5,20,211,8,20,10,20,12,
        20,214,9,20,1,21,1,21,1,21,5,21,219,8,21,10,21,12,21,222,9,21,1,
        22,1,22,1,22,5,22,227,8,22,10,22,12,22,230,9,22,1,23,1,23,1,23,5,
        23,235,8,23,10,23,12,23,238,9,23,1,24,1,24,1,24,3,24,243,8,24,1,
        25,1,25,1,25,1,25,1,25,3,25,250,8,25,1,25,3,25,253,8,25,5,25,255,
        8,25,10,25,12,25,258,9,25,1,26,1,26,1,26,3,26,263,8,26,1,26,1,26,
        1,26,1,26,1,26,3,26,270,8,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,
        1,26,1,26,1,26,1,26,1,26,3,26,284,8,26,1,26,0,1,2,27,0,2,4,6,8,10,
        12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,0,
        7,1,0,20,33,1,0,20,24,1,0,31,32,1,0,25,30,1,0,20,21,1,0,22,24,2,
        0,20,21,33,33,304,0,57,1,0,0,0,2,62,1,0,0,0,4,78,1,0,0,0,6,87,1,
        0,0,0,8,89,1,0,0,0,10,98,1,0,0,0,12,110,1,0,0,0,14,115,1,0,0,0,16,
        118,1,0,0,0,18,122,1,0,0,0,20,125,1,0,0,0,22,141,1,0,0,0,24,144,
        1,0,0,0,26,171,1,0,0,0,28,173,1,0,0,0,30,175,1,0,0,0,32,184,1,0,
        0,0,34,189,1,0,0,0,36,197,1,0,0,0,38,199,1,0,0,0,40,207,1,0,0,0,
        42,215,1,0,0,0,44,223,1,0,0,0,46,231,1,0,0,0,48,242,1,0,0,0,50,244,
        1,0,0,0,52,283,1,0,0,0,54,56,3,4,2,0,55,54,1,0,0,0,56,59,1,0,0,0,
        57,55,1,0,0,0,57,58,1,0,0,0,58,60,1,0,0,0,59,57,1,0,0,0,60,61,5,
        0,0,1,61,1,1,0,0,0,62,63,6,1,-1,0,63,64,5,19,0,0,64,69,1,0,0,0,65,
        66,10,1,0,0,66,68,5,42,0,0,67,65,1,0,0,0,68,71,1,0,0,0,69,67,1,0,
        0,0,69,70,1,0,0,0,70,3,1,0,0,0,71,69,1,0,0,0,72,79,3,26,13,0,73,
        79,3,24,12,0,74,79,3,16,8,0,75,79,3,10,5,0,76,79,3,18,9,0,77,79,
        3,36,18,0,78,72,1,0,0,0,78,73,1,0,0,0,78,74,1,0,0,0,78,75,1,0,0,
        0,78,76,1,0,0,0,78,77,1,0,0,0,79,5,1,0,0,0,80,88,3,4,2,0,81,83,5,
        8,0,0,82,84,3,36,18,0,83,82,1,0,0,0,83,84,1,0,0,0,84,88,1,0,0,0,
        85,88,5,11,0,0,86,88,5,12,0,0,87,80,1,0,0,0,87,81,1,0,0,0,87,85,
        1,0,0,0,87,86,1,0,0,0,88,7,1,0,0,0,89,93,5,39,0,0,90,92,3,6,3,0,
        91,90,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,0,93,94,1,0,0,0,94,96,1,
        0,0,0,95,93,1,0,0,0,96,97,5,40,0,0,97,9,1,0,0,0,98,99,5,1,0,0,99,
        100,3,36,18,0,100,104,3,8,4,0,101,103,3,12,6,0,102,101,1,0,0,0,103,
        106,1,0,0,0,104,102,1,0,0,0,104,105,1,0,0,0,105,108,1,0,0,0,106,
        104,1,0,0,0,107,109,3,14,7,0,108,107,1,0,0,0,108,109,1,0,0,0,109,
        11,1,0,0,0,110,111,5,5,0,0,111,112,5,1,0,0,112,113,3,36,18,0,113,
        114,3,8,4,0,114,13,1,0,0,0,115,116,5,5,0,0,116,117,3,8,4,0,117,15,
        1,0,0,0,118,119,5,10,0,0,119,120,3,36,18,0,120,121,3,8,4,0,121,17,
        1,0,0,0,122,123,5,3,0,0,123,124,5,16,0,0,124,19,1,0,0,0,125,126,
        5,7,0,0,126,127,3,36,18,0,127,21,1,0,0,0,128,129,3,2,1,0,129,130,
        5,34,0,0,130,132,1,0,0,0,131,128,1,0,0,0,131,132,1,0,0,0,132,133,
        1,0,0,0,133,142,5,19,0,0,134,142,7,0,0,0,135,136,3,2,1,0,136,137,
        5,34,0,0,137,139,1,0,0,0,138,135,1,0,0,0,138,139,1,0,0,0,139,140,
        1,0,0,0,140,142,5,2,0,0,141,131,1,0,0,0,141,134,1,0,0,0,141,138,
        1,0,0,0,142,23,1,0,0,0,143,145,5,9,0,0,144,143,1,0,0,0,144,145,1,
        0,0,0,145,146,1,0,0,0,146,147,5,4,0,0,147,148,3,22,11,0,148,150,
        5,37,0,0,149,151,3,34,17,0,150,149,1,0,0,0,150,151,1,0,0,0,151,152,
        1,0,0,0,152,155,5,38,0,0,153,154,5,41,0,0,154,156,3,2,1,0,155,153,
        1,0,0,0,155,156,1,0,0,0,156,157,1,0,0,0,157,158,3,8,4,0,158,25,1,
        0,0,0,159,161,5,19,0,0,160,162,7,1,0,0,161,160,1,0,0,0,161,162,1,
        0,0,0,162,163,1,0,0,0,163,164,5,36,0,0,164,172,3,36,18,0,165,167,
        5,6,0,0,166,165,1,0,0,0,166,167,1,0,0,0,167,168,1,0,0,0,168,169,
        5,19,0,0,169,170,5,36,0,0,170,172,3,36,18,0,171,159,1,0,0,0,171,
        166,1,0,0,0,172,27,1,0,0,0,173,174,3,36,18,0,174,29,1,0,0,0,175,
        180,3,28,14,0,176,177,5,35,0,0,177,179,3,28,14,0,178,176,1,0,0,0,
        179,182,1,0,0,0,180,178,1,0,0,0,180,181,1,0,0,0,181,31,1,0,0,0,182,
        180,1,0,0,0,183,185,5,6,0,0,184,183,1,0,0,0,184,185,1,0,0,0,185,
        186,1,0,0,0,186,187,3,2,1,0,187,188,5,19,0,0,188,33,1,0,0,0,189,
        194,3,32,16,0,190,191,5,35,0,0,191,193,3,32,16,0,192,190,1,0,0,0,
        193,196,1,0,0,0,194,192,1,0,0,0,194,195,1,0,0,0,195,35,1,0,0,0,196,
        194,1,0,0,0,197,198,3,38,19,0,198,37,1,0,0,0,199,205,3,40,20,0,200,
        201,5,1,0,0,201,202,3,40,20,0,202,203,5,5,0,0,203,204,3,40,20,0,
        204,206,1,0,0,0,205,200,1,0,0,0,205,206,1,0,0,0,206,39,1,0,0,0,207,
        212,3,42,21,0,208,209,7,2,0,0,209,211,3,42,21,0,210,208,1,0,0,0,
        211,214,1,0,0,0,212,210,1,0,0,0,212,213,1,0,0,0,213,41,1,0,0,0,214,
        212,1,0,0,0,215,220,3,44,22,0,216,217,7,3,0,0,217,219,3,44,22,0,
        218,216,1,0,0,0,219,222,1,0,0,0,220,218,1,0,0,0,220,221,1,0,0,0,
        221,43,1,0,0,0,222,220,1,0,0,0,223,228,3,46,23,0,224,225,7,4,0,0,
        225,227,3,46,23,0,226,224,1,0,0,0,227,230,1,0,0,0,228,226,1,0,0,
        0,228,229,1,0,0,0,229,45,1,0,0,0,230,228,1,0,0,0,231,236,3,48,24,
        0,232,233,7,5,0,0,233,235,3,48,24,0,234,232,1,0,0,0,235,238,1,0,
        0,0,236,234,1,0,0,0,236,237,1,0,0,0,237,47,1,0,0,0,238,236,1,0,0,
        0,239,240,7,6,0,0,240,243,3,48,24,0,241,243,3,50,25,0,242,239,1,
        0,0,0,242,241,1,0,0,0,243,49,1,0,0,0,244,256,3,52,26,0,245,246,5,
        34,0,0,246,252,5,19,0,0,247,249,5,37,0,0,248,250,3,30,15,0,249,248,
        1,0,0,0,249,250,1,0,0,0,250,251,1,0,0,0,251,253,5,38,0,0,252,247,
        1,0,0,0,252,253,1,0,0,0,253,255,1,0,0,0,254,245,1,0,0,0,255,258,
        1,0,0,0,256,254,1,0,0,0,256,257,1,0,0,0,257,51,1,0,0,0,258,256,1,
        0,0,0,259,260,5,19,0,0,260,262,5,37,0,0,261,263,3,30,15,0,262,261,
        1,0,0,0,262,263,1,0,0,0,263,264,1,0,0,0,264,284,5,38,0,0,265,266,
        5,2,0,0,266,267,3,2,1,0,267,269,5,37,0,0,268,270,3,30,15,0,269,268,
        1,0,0,0,269,270,1,0,0,0,270,271,1,0,0,0,271,272,5,38,0,0,272,284,
        1,0,0,0,273,274,5,37,0,0,274,275,3,36,18,0,275,276,5,38,0,0,276,
        284,1,0,0,0,277,284,5,14,0,0,278,284,5,15,0,0,279,284,5,16,0,0,280,
        284,5,17,0,0,281,284,5,18,0,0,282,284,5,19,0,0,283,259,1,0,0,0,283,
        265,1,0,0,0,283,273,1,0,0,0,283,277,1,0,0,0,283,278,1,0,0,0,283,
        279,1,0,0,0,283,280,1,0,0,0,283,281,1,0,0,0,283,282,1,0,0,0,284,
        53,1,0,0,0,32,57,69,78,83,87,93,104,108,131,138,141,144,150,155,
        161,166,171,180,184,194,205,212,220,228,236,242,249,252,256,262,
        269,283
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
                     "'.'", "','", "'='", "'('", "')'", "'{'", "'}'", "'->'", 
                     "'&'" ]

    symbolicNames = [ "<INVALID>", "IF", "NEW", "USE", "FUNC", "ELSE", "MUTABLE", 
                      "DEFER", "RETURN", "STATIC", "WHILE", "BREAK", "CONTINUE", 
                      "APOSTROPHE", "INT", "FLOAT", "STRING", "STRING_POINTER", 
                      "BOOL", "ID", "ADD", "SUB", "MUL", "DIV", "MOD", "EEQ", 
                      "NEQ", "GT", "LT", "GTE", "LTE", "AND", "OR", "NOT", 
                      "DOT", "COMMA", "ASSIGN", "LPAREN", "RPAREN", "LBRACE", 
                      "RBRACE", "RETURNS", "AMPERSAND", "COMMENT", "MULTILINE_COMMENT", 
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
    AMPERSAND=42
    COMMENT=43
    MULTILINE_COMMENT=44
    WHITESPACE=45
    OTHER=46

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

        def type_(self):
            return self.getTypedRuleContext(ByteParser.TypeContext,0)


        def AMPERSAND(self):
            return self.getToken(ByteParser.AMPERSAND, 0)

        def getRuleIndex(self):
            return ByteParser.RULE_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)



    def type_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ByteParser.TypeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_type, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(ByteParser.ID)
            self._ctx.stop = self._input.LT(-1)
            self.state = 69
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ByteParser.TypeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                    self.state = 65
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 66
                    self.match(ByteParser.AMPERSAND) 
                self.state = 71
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
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
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 72
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 73
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 74
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 75
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 76
                self.useStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 77
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
            self.state = 87
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 6, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21, 33, 37]:
                localctx = ByteParser.BodyStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 80
                self.stmt()
                pass
            elif token in [8]:
                localctx = ByteParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 81
                self.match(ByteParser.RETURN)
                self.state = 83
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                if la_ == 1:
                    self.state = 82
                    self.expr()


                pass
            elif token in [11]:
                localctx = ByteParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 85
                self.match(ByteParser.BREAK)
                pass
            elif token in [12]:
                localctx = ByteParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 86
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
            self.state = 89
            self.match(ByteParser.LBRACE)
            self.state = 93
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033074014) != 0):
                self.state = 90
                self.bodyStmts()
                self.state = 95
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 96
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
            self.state = 98
            self.match(ByteParser.IF)
            self.state = 99
            self.expr()
            self.state = 100
            self.body()
            self.state = 104
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 101
                    self.elseifStmt() 
                self.state = 106
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 108
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 107
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
            self.state = 110
            self.match(ByteParser.ELSE)
            self.state = 111
            self.match(ByteParser.IF)
            self.state = 112
            self.expr()
            self.state = 113
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
            self.state = 115
            self.match(ByteParser.ELSE)
            self.state = 116
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
            self.state = 118
            self.match(ByteParser.WHILE)
            self.state = 119
            self.expr()
            self.state = 120
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
            self.state = 122
            self.match(ByteParser.USE)
            self.state = 123
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
            self.state = 125
            self.match(ByteParser.DEFER)
            self.state = 126
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
            self.state = 141
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 128
                    localctx.extend_type = self.type_(0)
                    self.state = 129
                    self.match(ByteParser.DOT)


                self.state = 133
                self.match(ByteParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 134
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
                self.state = 138
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==19:
                    self.state = 135
                    localctx.extend_type = self.type_(0)
                    self.state = 136
                    self.match(ByteParser.DOT)


                self.state = 140
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
            self.state = 144
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 143
                self.match(ByteParser.STATIC)


            self.state = 146
            self.match(ByteParser.FUNC)
            self.state = 147
            self.funcName()
            self.state = 148
            self.match(ByteParser.LPAREN)
            self.state = 150
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6 or _la==19:
                self.state = 149
                self.params()


            self.state = 152
            self.match(ByteParser.RPAREN)
            self.state = 155
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 153
                self.match(ByteParser.RETURNS)
                self.state = 154
                localctx.return_type = self.type_(0)


            self.state = 157
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
            self.state = 171
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 159
                self.match(ByteParser.ID)
                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32505856) != 0):
                    self.state = 160
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 32505856) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 163
                self.match(ByteParser.ASSIGN)
                self.state = 164
                self.expr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 165
                    self.match(ByteParser.MUTABLE)


                self.state = 168
                self.match(ByteParser.ID)
                self.state = 169
                self.match(ByteParser.ASSIGN)
                self.state = 170
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
            self.state = 173
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
            self.state = 175
            self.arg()
            self.state = 180
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 176
                self.match(ByteParser.COMMA)
                self.state = 177
                self.arg()
                self.state = 182
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
            self.state = 184
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 183
                self.match(ByteParser.MUTABLE)


            self.state = 186
            self.type_(0)
            self.state = 187
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
            self.state = 189
            self.param()
            self.state = 194
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 190
                self.match(ByteParser.COMMA)
                self.state = 191
                self.param()
                self.state = 196
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
            self.state = 197
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
            self.state = 199
            self.logical()
            self.state = 205
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 200
                self.match(ByteParser.IF)
                self.state = 201
                self.logical()
                self.state = 202
                self.match(ByteParser.ELSE)
                self.state = 203
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
            self.state = 207
            self.relational()
            self.state = 212
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31 or _la==32:
                self.state = 208
                _la = self._input.LA(1)
                if not(_la==31 or _la==32):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 209
                self.relational()
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
            self.state = 215
            self.addition()
            self.state = 220
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2113929216) != 0):
                self.state = 216
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2113929216) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 217
                self.addition()
                self.state = 222
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
            self.state = 223
            self.multiplication()
            self.state = 228
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,23,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 224
                    _la = self._input.LA(1)
                    if not(_la==20 or _la==21):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 225
                    self.multiplication() 
                self.state = 230
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,23,self._ctx)

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
            self.state = 231
            self.unary()
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 29360128) != 0):
                self.state = 232
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 29360128) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 233
                self.unary()
                self.state = 238
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
            self.state = 242
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20, 21, 33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 239
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8593080320) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 240
                self.unary()
                pass
            elif token in [2, 14, 15, 16, 17, 18, 19, 37]:
                self.enterOuterAlt(localctx, 2)
                self.state = 241
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
            self.state = 244
            self.primary()
            self.state = 256
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 245
                self.match(ByteParser.DOT)
                self.state = 246
                self.match(ByteParser.ID)
                self.state = 252
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
                if la_ == 1:
                    self.state = 247
                    self.match(ByteParser.LPAREN)
                    self.state = 249
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033065988) != 0):
                        self.state = 248
                        self.args()


                    self.state = 251
                    self.match(ByteParser.RPAREN)


                self.state = 258
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
            self.state = 283
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                localctx = ByteParser.CallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 259
                self.match(ByteParser.ID)
                self.state = 260
                self.match(ByteParser.LPAREN)
                self.state = 262
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033065988) != 0):
                    self.state = 261
                    self.args()


                self.state = 264
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = ByteParser.NewContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 265
                self.match(ByteParser.NEW)
                self.state = 266
                self.type_(0)
                self.state = 267
                self.match(ByteParser.LPAREN)
                self.state = 269
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 146033065988) != 0):
                    self.state = 268
                    self.args()


                self.state = 271
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = ByteParser.ParenContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 273
                self.match(ByteParser.LPAREN)
                self.state = 274
                self.expr()
                self.state = 275
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = ByteParser.IntContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 277
                self.match(ByteParser.INT)
                pass

            elif la_ == 5:
                localctx = ByteParser.FloatContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 278
                self.match(ByteParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = ByteParser.StringContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 279
                self.match(ByteParser.STRING)
                pass

            elif la_ == 7:
                localctx = ByteParser.StringPointerContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 280
                self.match(ByteParser.STRING_POINTER)
                pass

            elif la_ == 8:
                localctx = ByteParser.BoolContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 281
                self.match(ByteParser.BOOL)
                pass

            elif la_ == 9:
                localctx = ByteParser.IdContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 282
                self.match(ByteParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.type_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def type_sempred(self, localctx:TypeContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         




