grammar Byte;

program: stmt* EOF;

type
    : ID
    | type AMPERSAND
    ;

stmt
    : varAssign | funcAssign | classAssign
    | whileStmt | ifStmt | useStmt | forRangeStmt | foreachStmt
    | expr
    ;

bodyStmts
    : stmt #bodyStmt
    | RETURN expr? #return
    | BREAK #break
    | CONTINUE #continue
    ;

body
    : LBRACE bodyStmts* RBRACE
    // | bodyStmts
    ;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
useStmt: USE STRING;
forRangeStmt: FOR ID IN expr DOUBLEDOT expr (DOUBLEDOT expr)? body;
foreachStmt: FOREACH ID IN expr body;

funcName
    : (extend_type=type DOT)? ID
    | op=(ADD | SUB | MUL | DIV | MOD | EEQ | NEQ | GT | LT | GTE | LTE | AND | OR | NOT)
    | (extend_type=type DOT)? NEW
    ;

genericParams: LT ID (COMMA ID)* GT;

funcAssign
    : STATIC? FUNC funcName genericParams? LPAREN params? RPAREN (RETURNS return_type=type)? body
    ;
varAssign
    : ID (DOT ID)? op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | MUTABLE? ID ASSIGN expr
    ;

propertyDecl: type ID;
methodDecl: funcAssign;

classAssign
    : CLASS ID LBRACE classDecl* RBRACE
    ;

classDecl
    : propertyDecl
    | methodDecl
    ;

arg: expr;
args: arg (COMMA arg)*;

param: MUTABLE? type ID;
params: param (COMMA param)*;

expr: ternary;

ternary: logical (IF logical ELSE logical)?;

logical: relational ((AND | OR) relational)*;

relational: addition ((EEQ | NEQ | GT | LT | GTE | LTE) addition)*;

addition: multiplication ((ADD | SUB) multiplication)*;

multiplication: unary ((MUL | DIV | MOD) unary)*;

unary
    : (NOT | ADD | SUB) unary
    | postfix
    ;

postfix: primary (DOT ID (LPAREN args? RPAREN)?)*;

primary
    : ID LPAREN args? RPAREN #call
    | NEW type LPAREN args? RPAREN #new
    | NEW type LBRACK INT RBRACK #newArray
    | LPAREN expr RPAREN #paren
    | INT #int
    | FLOAT #float
    | STRING #string
    | STRING_POINTER #stringPointer
    | BOOL #bool
    | ID #id
    ;


// Basic keywords
IF: 'if';
IN: 'in';
FOR: 'for';
NEW: 'new';
USE: 'use';
FUNC: 'fn';
ELSE: 'else';
CLASS: 'class';
MUTABLE: 'mut';
RETURN: 'return';
STATIC: 'static';
FOREACH: 'foreach';

// Loop keywords
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

INT: [0-9]+;
FLOAT: [0-9]* '.' [0-9]+;
STRING
    : '"' (~["\\\r\n] | '\\' .)* '"'
    | '\'' (~['\\\r\n] | '\\' .)* '\''
    ;
STRING_POINTER: 'p' STRING;
BOOL: 'true' | 'false';
ID: [a-zA-Z_][a-zA-Z_0-9]*;

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';
EEQ: '==';
NEQ: '!=';
GT: '>';
LT: '<';
GTE: '>=';
LTE: '<=';
AND: '&&';
OR: '||';
NOT: '!';

DOT: '.';
COMMA: ',';
ASSIGN: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
RETURNS: '->';
AMPERSAND: '&';
DOUBLEDOT: '..';

COMMENT: '//' ~[\r\n]* '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
