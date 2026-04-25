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
        4,1,49,303,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,1,0,5,0,58,8,0,10,0,12,0,61,9,0,1,0,1,0,1,1,1,1,1,1,1,
        1,1,1,5,1,70,8,1,10,1,12,1,73,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,
        2,82,8,2,1,3,1,3,1,3,3,3,87,8,3,1,3,1,3,3,3,91,8,3,1,4,1,4,5,4,95,
        8,4,10,4,12,4,98,9,4,1,4,1,4,3,4,102,8,4,1,5,1,5,1,5,1,5,5,5,108,
        8,5,10,5,12,5,111,9,5,1,5,3,5,114,8,5,1,6,1,6,1,6,1,6,1,6,1,7,1,
        7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,3,11,142,8,11,1,11,1,11,1,12,1,12,1,12,
        3,12,149,8,12,1,12,1,12,1,12,1,12,1,12,3,12,156,8,12,1,12,3,12,159,
        8,12,1,13,3,13,162,8,13,1,13,1,13,1,13,1,13,3,13,168,8,13,1,13,1,
        13,1,13,3,13,173,8,13,1,13,1,13,1,14,1,14,3,14,179,8,14,1,14,1,14,
        1,14,3,14,184,8,14,1,14,1,14,1,14,3,14,189,8,14,1,15,1,15,1,16,1,
        16,1,16,5,16,196,8,16,10,16,12,16,199,9,16,1,17,3,17,202,8,17,1,
        17,1,17,1,17,1,18,1,18,1,18,5,18,210,8,18,10,18,12,18,213,9,18,1,
        19,1,19,1,20,1,20,1,20,1,20,1,20,1,20,3,20,223,8,20,1,21,1,21,1,
        21,5,21,228,8,21,10,21,12,21,231,9,21,1,22,1,22,1,22,5,22,236,8,
        22,10,22,12,22,239,9,22,1,23,1,23,1,23,5,23,244,8,23,10,23,12,23,
        247,9,23,1,24,1,24,1,24,5,24,252,8,24,10,24,12,24,255,9,24,1,25,
        1,25,1,25,3,25,260,8,25,1,26,1,26,1,26,1,26,1,26,3,26,267,8,26,1,
        26,3,26,270,8,26,5,26,272,8,26,10,26,12,26,275,9,26,1,27,1,27,1,
        27,3,27,280,8,27,1,27,1,27,1,27,1,27,1,27,3,27,287,8,27,1,27,1,27,
        1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,3,27,301,8,27,
        1,27,0,1,2,28,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        38,40,42,44,46,48,50,52,54,0,7,1,0,22,35,1,0,22,26,1,0,33,34,1,0,
        27,32,1,0,22,23,1,0,24,26,2,0,22,23,35,35,323,0,59,1,0,0,0,2,64,
        1,0,0,0,4,81,1,0,0,0,6,90,1,0,0,0,8,101,1,0,0,0,10,103,1,0,0,0,12,
        115,1,0,0,0,14,120,1,0,0,0,16,123,1,0,0,0,18,127,1,0,0,0,20,130,
        1,0,0,0,22,133,1,0,0,0,24,158,1,0,0,0,26,161,1,0,0,0,28,188,1,0,
        0,0,30,190,1,0,0,0,32,192,1,0,0,0,34,201,1,0,0,0,36,206,1,0,0,0,
        38,214,1,0,0,0,40,216,1,0,0,0,42,224,1,0,0,0,44,232,1,0,0,0,46,240,
        1,0,0,0,48,248,1,0,0,0,50,259,1,0,0,0,52,261,1,0,0,0,54,300,1,0,
        0,0,56,58,3,4,2,0,57,56,1,0,0,0,58,61,1,0,0,0,59,57,1,0,0,0,59,60,
        1,0,0,0,60,62,1,0,0,0,61,59,1,0,0,0,62,63,5,0,0,1,63,1,1,0,0,0,64,
        65,6,1,-1,0,65,66,5,21,0,0,66,71,1,0,0,0,67,68,10,1,0,0,68,70,5,
        44,0,0,69,67,1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,
        3,1,0,0,0,73,71,1,0,0,0,74,82,3,28,14,0,75,82,3,26,13,0,76,82,3,
        16,8,0,77,82,3,10,5,0,78,82,3,18,9,0,79,82,3,22,11,0,80,82,3,38,
        19,0,81,74,1,0,0,0,81,75,1,0,0,0,81,76,1,0,0,0,81,77,1,0,0,0,81,
        78,1,0,0,0,81,79,1,0,0,0,81,80,1,0,0,0,82,5,1,0,0,0,83,91,3,4,2,
        0,84,86,5,10,0,0,85,87,3,38,19,0,86,85,1,0,0,0,86,87,1,0,0,0,87,
        91,1,0,0,0,88,91,5,13,0,0,89,91,5,14,0,0,90,83,1,0,0,0,90,84,1,0,
        0,0,90,88,1,0,0,0,90,89,1,0,0,0,91,7,1,0,0,0,92,96,5,41,0,0,93,95,
        3,6,3,0,94,93,1,0,0,0,95,98,1,0,0,0,96,94,1,0,0,0,96,97,1,0,0,0,
        97,99,1,0,0,0,98,96,1,0,0,0,99,102,5,42,0,0,100,102,3,6,3,0,101,
        92,1,0,0,0,101,100,1,0,0,0,102,9,1,0,0,0,103,104,5,1,0,0,104,105,
        3,38,19,0,105,109,3,8,4,0,106,108,3,12,6,0,107,106,1,0,0,0,108,111,
        1,0,0,0,109,107,1,0,0,0,109,110,1,0,0,0,110,113,1,0,0,0,111,109,
        1,0,0,0,112,114,3,14,7,0,113,112,1,0,0,0,113,114,1,0,0,0,114,11,
        1,0,0,0,115,116,5,7,0,0,116,117,5,1,0,0,117,118,3,38,19,0,118,119,
        3,8,4,0,119,13,1,0,0,0,120,121,5,7,0,0,121,122,3,8,4,0,122,15,1,
        0,0,0,123,124,5,12,0,0,124,125,3,38,19,0,125,126,3,8,4,0,126,17,
        1,0,0,0,127,128,5,5,0,0,128,129,5,18,0,0,129,19,1,0,0,0,130,131,
        5,9,0,0,131,132,3,38,19,0,132,21,1,0,0,0,133,134,5,3,0,0,134,135,
        5,21,0,0,135,136,5,2,0,0,136,137,3,38,19,0,137,138,5,45,0,0,138,
        141,3,38,19,0,139,140,5,45,0,0,140,142,3,38,19,0,141,139,1,0,0,0,
        141,142,1,0,0,0,142,143,1,0,0,0,143,144,3,8,4,0,144,23,1,0,0,0,145,
        146,3,2,1,0,146,147,5,36,0,0,147,149,1,0,0,0,148,145,1,0,0,0,148,
        149,1,0,0,0,149,150,1,0,0,0,150,159,5,21,0,0,151,159,7,0,0,0,152,
        153,3,2,1,0,153,154,5,36,0,0,154,156,1,0,0,0,155,152,1,0,0,0,155,
        156,1,0,0,0,156,157,1,0,0,0,157,159,5,4,0,0,158,148,1,0,0,0,158,
        151,1,0,0,0,158,155,1,0,0,0,159,25,1,0,0,0,160,162,5,11,0,0,161,
        160,1,0,0,0,161,162,1,0,0,0,162,163,1,0,0,0,163,164,5,6,0,0,164,
        165,3,24,12,0,165,167,5,39,0,0,166,168,3,36,18,0,167,166,1,0,0,0,
        167,168,1,0,0,0,168,169,1,0,0,0,169,172,5,40,0,0,170,171,5,43,0,
        0,171,173,3,2,1,0,172,170,1,0,0,0,172,173,1,0,0,0,173,174,1,0,0,
        0,174,175,3,8,4,0,175,27,1,0,0,0,176,178,5,21,0,0,177,179,7,1,0,
        0,178,177,1,0,0,0,178,179,1,0,0,0,179,180,1,0,0,0,180,181,5,38,0,
        0,181,189,3,38,19,0,182,184,5,8,0,0,183,182,1,0,0,0,183,184,1,0,
        0,0,184,185,1,0,0,0,185,186,5,21,0,0,186,187,5,38,0,0,187,189,3,
        38,19,0,188,176,1,0,0,0,188,183,1,0,0,0,189,29,1,0,0,0,190,191,3,
        38,19,0,191,31,1,0,0,0,192,197,3,30,15,0,193,194,5,37,0,0,194,196,
        3,30,15,0,195,193,1,0,0,0,196,199,1,0,0,0,197,195,1,0,0,0,197,198,
        1,0,0,0,198,33,1,0,0,0,199,197,1,0,0,0,200,202,5,8,0,0,201,200,1,
        0,0,0,201,202,1,0,0,0,202,203,1,0,0,0,203,204,3,2,1,0,204,205,5,
        21,0,0,205,35,1,0,0,0,206,211,3,34,17,0,207,208,5,37,0,0,208,210,
        3,34,17,0,209,207,1,0,0,0,210,213,1,0,0,0,211,209,1,0,0,0,211,212,
        1,0,0,0,212,37,1,0,0,0,213,211,1,0,0,0,214,215,3,40,20,0,215,39,
        1,0,0,0,216,222,3,42,21,0,217,218,5,1,0,0,218,219,3,42,21,0,219,
        220,5,7,0,0,220,221,3,42,21,0,221,223,1,0,0,0,222,217,1,0,0,0,222,
        223,1,0,0,0,223,41,1,0,0,0,224,229,3,44,22,0,225,226,7,2,0,0,226,
        228,3,44,22,0,227,225,1,0,0,0,228,231,1,0,0,0,229,227,1,0,0,0,229,
        230,1,0,0,0,230,43,1,0,0,0,231,229,1,0,0,0,232,237,3,46,23,0,233,
        234,7,3,0,0,234,236,3,46,23,0,235,233,1,0,0,0,236,239,1,0,0,0,237,
        235,1,0,0,0,237,238,1,0,0,0,238,45,1,0,0,0,239,237,1,0,0,0,240,245,
        3,48,24,0,241,242,7,4,0,0,242,244,3,48,24,0,243,241,1,0,0,0,244,
        247,1,0,0,0,245,243,1,0,0,0,245,246,1,0,0,0,246,47,1,0,0,0,247,245,
        1,0,0,0,248,253,3,50,25,0,249,250,7,5,0,0,250,252,3,50,25,0,251,
        249,1,0,0,0,252,255,1,0,0,0,253,251,1,0,0,0,253,254,1,0,0,0,254,
        49,1,0,0,0,255,253,1,0,0,0,256,257,7,6,0,0,257,260,3,50,25,0,258,
        260,3,52,26,0,259,256,1,0,0,0,259,258,1,0,0,0,260,51,1,0,0,0,261,
        273,3,54,27,0,262,263,5,36,0,0,263,269,5,21,0,0,264,266,5,39,0,0,
        265,267,3,32,16,0,266,265,1,0,0,0,266,267,1,0,0,0,267,268,1,0,0,
        0,268,270,5,40,0,0,269,264,1,0,0,0,269,270,1,0,0,0,270,272,1,0,0,
        0,271,262,1,0,0,0,272,275,1,0,0,0,273,271,1,0,0,0,273,274,1,0,0,
        0,274,53,1,0,0,0,275,273,1,0,0,0,276,277,5,21,0,0,277,279,5,39,0,
        0,278,280,3,32,16,0,279,278,1,0,0,0,279,280,1,0,0,0,280,281,1,0,
        0,0,281,301,5,40,0,0,282,283,5,4,0,0,283,284,3,2,1,0,284,286,5,39,
        0,0,285,287,3,32,16,0,286,285,1,0,0,0,286,287,1,0,0,0,287,288,1,
        0,0,0,288,289,5,40,0,0,289,301,1,0,0,0,290,291,5,39,0,0,291,292,
        3,38,19,0,292,293,5,40,0,0,293,301,1,0,0,0,294,301,5,16,0,0,295,
        301,5,17,0,0,296,301,5,18,0,0,297,301,5,19,0,0,298,301,5,20,0,0,
        299,301,5,21,0,0,300,276,1,0,0,0,300,282,1,0,0,0,300,290,1,0,0,0,
        300,294,1,0,0,0,300,295,1,0,0,0,300,296,1,0,0,0,300,297,1,0,0,0,
        300,298,1,0,0,0,300,299,1,0,0,0,301,55,1,0,0,0,34,59,71,81,86,90,
        96,101,109,113,141,148,155,158,161,167,172,178,183,188,197,201,211,
        222,229,237,245,253,259,266,269,273,279,286,300
    ]

class ByteParser ( Parser ):

    grammarFileName = "Byte.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'in'", "'for'", "'new'", "'use'", 
                     "'fn'", "'else'", "'mut'", "'defer'", "'return'", "'static'", 
                     "'while'", "'break'", "'continue'", "'''", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'%'", "'=='", 
                     "'!='", "'>'", "'<'", "'>='", "'<='", "'&&'", "'||'", 
                     "'!'", "'.'", "','", "'='", "'('", "')'", "'{'", "'}'", 
                     "'->'", "'&'", "'..'" ]

    symbolicNames = [ "<INVALID>", "IF", "IN", "FOR", "NEW", "USE", "FUNC", 
                      "ELSE", "MUTABLE", "DEFER", "RETURN", "STATIC", "WHILE", 
                      "BREAK", "CONTINUE", "APOSTROPHE", "INT", "FLOAT", 
                      "STRING", "STRING_POINTER", "BOOL", "ID", "ADD", "SUB", 
                      "MUL", "DIV", "MOD", "EEQ", "NEQ", "GT", "LT", "GTE", 
                      "LTE", "AND", "OR", "NOT", "DOT", "COMMA", "ASSIGN", 
                      "LPAREN", "RPAREN", "LBRACE", "RBRACE", "RETURNS", 
                      "AMPERSAND", "DOUBLEDOT", "COMMENT", "MULTILINE_COMMENT", 
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
    RULE_forRangeStmt = 11
    RULE_funcName = 12
    RULE_funcAssign = 13
    RULE_varAssign = 14
    RULE_arg = 15
    RULE_args = 16
    RULE_param = 17
    RULE_params = 18
    RULE_expr = 19
    RULE_ternary = 20
    RULE_logical = 21
    RULE_relational = 22
    RULE_addition = 23
    RULE_multiplication = 24
    RULE_unary = 25
    RULE_postfix = 26
    RULE_primary = 27

    ruleNames =  [ "program", "type", "stmt", "bodyStmts", "body", "ifStmt", 
                   "elseifStmt", "elseStmt", "whileStmt", "useStmt", "deferStmt", 
                   "forRangeStmt", "funcName", "funcAssign", "varAssign", 
                   "arg", "args", "param", "params", "expr", "ternary", 
                   "logical", "relational", "addition", "multiplication", 
                   "unary", "postfix", "primary" ]

    EOF = Token.EOF
    IF=1
    IN=2
    FOR=3
    NEW=4
    USE=5
    FUNC=6
    ELSE=7
    MUTABLE=8
    DEFER=9
    RETURN=10
    STATIC=11
    WHILE=12
    BREAK=13
    CONTINUE=14
    APOSTROPHE=15
    INT=16
    FLOAT=17
    STRING=18
    STRING_POINTER=19
    BOOL=20
    ID=21
    ADD=22
    SUB=23
    MUL=24
    DIV=25
    MOD=26
    EEQ=27
    NEQ=28
    GT=29
    LT=30
    GTE=31
    LTE=32
    AND=33
    OR=34
    NOT=35
    DOT=36
    COMMA=37
    ASSIGN=38
    LPAREN=39
    RPAREN=40
    LBRACE=41
    RBRACE=42
    RETURNS=43
    AMPERSAND=44
    DOUBLEDOT=45
    COMMENT=46
    MULTILINE_COMMENT=47
    WHITESPACE=48
    OTHER=49

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
            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 584132270458) != 0):
                self.state = 56
                self.stmt()
                self.state = 61
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 62
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
            self.state = 65
            self.match(ByteParser.ID)
            self._ctx.stop = self._input.LT(-1)
            self.state = 71
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ByteParser.TypeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                    self.state = 67
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 68
                    self.match(ByteParser.AMPERSAND) 
                self.state = 73
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


        def forRangeStmt(self):
            return self.getTypedRuleContext(ByteParser.ForRangeStmtContext,0)


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
            self.state = 81
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 76
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 77
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 78
                self.useStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 79
                self.forRangeStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 80
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
            self.state = 90
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 6, 8, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 35, 39]:
                localctx = ByteParser.BodyStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 83
                self.stmt()
                pass
            elif token in [10]:
                localctx = ByteParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 84
                self.match(ByteParser.RETURN)
                self.state = 86
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                if la_ == 1:
                    self.state = 85
                    self.expr()


                pass
            elif token in [13]:
                localctx = ByteParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 88
                self.match(ByteParser.BREAK)
                pass
            elif token in [14]:
                localctx = ByteParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 89
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
            self.state = 101
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41]:
                self.enterOuterAlt(localctx, 1)
                self.state = 92
                self.match(ByteParser.LBRACE)
                self.state = 96
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 584132296058) != 0):
                    self.state = 93
                    self.bodyStmts()
                    self.state = 98
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 99
                self.match(ByteParser.RBRACE)
                pass
            elif token in [1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 35, 39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 100
                self.bodyStmts()
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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.match(ByteParser.IF)
            self.state = 104
            self.expr()
            self.state = 105
            self.body()
            self.state = 109
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 106
                    self.elseifStmt() 
                self.state = 111
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 113
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 112
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
            self.state = 115
            self.match(ByteParser.ELSE)
            self.state = 116
            self.match(ByteParser.IF)
            self.state = 117
            self.expr()
            self.state = 118
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
            self.state = 120
            self.match(ByteParser.ELSE)
            self.state = 121
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
            self.state = 123
            self.match(ByteParser.WHILE)
            self.state = 124
            self.expr()
            self.state = 125
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
            self.state = 127
            self.match(ByteParser.USE)
            self.state = 128
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
            self.state = 130
            self.match(ByteParser.DEFER)
            self.state = 131
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForRangeStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(ByteParser.FOR, 0)

        def ID(self):
            return self.getToken(ByteParser.ID, 0)

        def IN(self):
            return self.getToken(ByteParser.IN, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ByteParser.ExprContext)
            else:
                return self.getTypedRuleContext(ByteParser.ExprContext,i)


        def DOUBLEDOT(self, i:int=None):
            if i is None:
                return self.getTokens(ByteParser.DOUBLEDOT)
            else:
                return self.getToken(ByteParser.DOUBLEDOT, i)

        def body(self):
            return self.getTypedRuleContext(ByteParser.BodyContext,0)


        def getRuleIndex(self):
            return ByteParser.RULE_forRangeStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForRangeStmt" ):
                return visitor.visitForRangeStmt(self)
            else:
                return visitor.visitChildren(self)




    def forRangeStmt(self):

        localctx = ByteParser.ForRangeStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_forRangeStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.match(ByteParser.FOR)
            self.state = 134
            self.match(ByteParser.ID)
            self.state = 135
            self.match(ByteParser.IN)
            self.state = 136
            self.expr()
            self.state = 137
            self.match(ByteParser.DOUBLEDOT)
            self.state = 138
            self.expr()
            self.state = 141
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 139
                self.match(ByteParser.DOUBLEDOT)
                self.state = 140
                self.expr()


            self.state = 143
            self.body()
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
        self.enterRule(localctx, 24, self.RULE_funcName)
        self._la = 0 # Token type
        try:
            self.state = 158
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 148
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
                if la_ == 1:
                    self.state = 145
                    localctx.extend_type = self.type_(0)
                    self.state = 146
                    self.match(ByteParser.DOT)


                self.state = 150
                self.match(ByteParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 151
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 68715282432) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 155
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==21:
                    self.state = 152
                    localctx.extend_type = self.type_(0)
                    self.state = 153
                    self.match(ByteParser.DOT)


                self.state = 157
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
        self.enterRule(localctx, 26, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 160
                self.match(ByteParser.STATIC)


            self.state = 163
            self.match(ByteParser.FUNC)
            self.state = 164
            self.funcName()
            self.state = 165
            self.match(ByteParser.LPAREN)
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8 or _la==21:
                self.state = 166
                self.params()


            self.state = 169
            self.match(ByteParser.RPAREN)
            self.state = 172
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 170
                self.match(ByteParser.RETURNS)
                self.state = 171
                localctx.return_type = self.type_(0)


            self.state = 174
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
        self.enterRule(localctx, 28, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.state = 188
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 176
                self.match(ByteParser.ID)
                self.state = 178
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 130023424) != 0):
                    self.state = 177
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 130023424) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 180
                self.match(ByteParser.ASSIGN)
                self.state = 181
                self.expr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 183
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==8:
                    self.state = 182
                    self.match(ByteParser.MUTABLE)


                self.state = 185
                self.match(ByteParser.ID)
                self.state = 186
                self.match(ByteParser.ASSIGN)
                self.state = 187
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
        self.enterRule(localctx, 30, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
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
        self.enterRule(localctx, 32, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.arg()
            self.state = 197
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==37:
                self.state = 193
                self.match(ByteParser.COMMA)
                self.state = 194
                self.arg()
                self.state = 199
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
        self.enterRule(localctx, 34, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 200
                self.match(ByteParser.MUTABLE)


            self.state = 203
            self.type_(0)
            self.state = 204
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
        self.enterRule(localctx, 36, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.param()
            self.state = 211
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==37:
                self.state = 207
                self.match(ByteParser.COMMA)
                self.state = 208
                self.param()
                self.state = 213
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
        self.enterRule(localctx, 38, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 214
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
        self.enterRule(localctx, 40, self.RULE_ternary)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            self.logical()
            self.state = 222
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.state = 217
                self.match(ByteParser.IF)
                self.state = 218
                self.logical()
                self.state = 219
                self.match(ByteParser.ELSE)
                self.state = 220
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
        self.enterRule(localctx, 42, self.RULE_logical)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            self.relational()
            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33 or _la==34:
                self.state = 225
                _la = self._input.LA(1)
                if not(_la==33 or _la==34):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 226
                self.relational()
                self.state = 231
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
        self.enterRule(localctx, 44, self.RULE_relational)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self.addition()
            self.state = 237
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8455716864) != 0):
                self.state = 233
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8455716864) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 234
                self.addition()
                self.state = 239
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
        self.enterRule(localctx, 46, self.RULE_addition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 240
            self.multiplication()
            self.state = 245
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,25,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 241
                    _la = self._input.LA(1)
                    if not(_la==22 or _la==23):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 242
                    self.multiplication() 
                self.state = 247
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,25,self._ctx)

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
        self.enterRule(localctx, 48, self.RULE_multiplication)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.unary()
            self.state = 253
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 117440512) != 0):
                self.state = 249
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 117440512) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 250
                self.unary()
                self.state = 255
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
        self.enterRule(localctx, 50, self.RULE_unary)
        self._la = 0 # Token type
        try:
            self.state = 259
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22, 23, 35]:
                self.enterOuterAlt(localctx, 1)
                self.state = 256
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 34372321280) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 257
                self.unary()
                pass
            elif token in [4, 16, 17, 18, 19, 20, 21, 39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 258
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
        self.enterRule(localctx, 52, self.RULE_postfix)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.primary()
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 262
                self.match(ByteParser.DOT)
                self.state = 263
                self.match(ByteParser.ID)
                self.state = 269
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
                if la_ == 1:
                    self.state = 264
                    self.match(ByteParser.LPAREN)
                    self.state = 266
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & 584132263952) != 0):
                        self.state = 265
                        self.args()


                    self.state = 268
                    self.match(ByteParser.RPAREN)


                self.state = 275
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
        self.enterRule(localctx, 54, self.RULE_primary)
        self._la = 0 # Token type
        try:
            self.state = 300
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                localctx = ByteParser.CallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 276
                self.match(ByteParser.ID)
                self.state = 277
                self.match(ByteParser.LPAREN)
                self.state = 279
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 584132263952) != 0):
                    self.state = 278
                    self.args()


                self.state = 281
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = ByteParser.NewContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 282
                self.match(ByteParser.NEW)
                self.state = 283
                self.type_(0)
                self.state = 284
                self.match(ByteParser.LPAREN)
                self.state = 286
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 584132263952) != 0):
                    self.state = 285
                    self.args()


                self.state = 288
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = ByteParser.ParenContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 290
                self.match(ByteParser.LPAREN)
                self.state = 291
                self.expr()
                self.state = 292
                self.match(ByteParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = ByteParser.IntContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 294
                self.match(ByteParser.INT)
                pass

            elif la_ == 5:
                localctx = ByteParser.FloatContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 295
                self.match(ByteParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = ByteParser.StringContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 296
                self.match(ByteParser.STRING)
                pass

            elif la_ == 7:
                localctx = ByteParser.StringPointerContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 297
                self.match(ByteParser.STRING_POINTER)
                pass

            elif la_ == 8:
                localctx = ByteParser.BoolContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 298
                self.match(ByteParser.BOOL)
                pass

            elif la_ == 9:
                localctx = ByteParser.IdContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 299
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
         




