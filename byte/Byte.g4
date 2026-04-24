grammar Byte;

program: stmt* EOF;

type
    : ID
    | type AMPERSAND
    ;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt | useStmt// | deferStmt
    | expr
    ;

bodyStmts
    : stmt #bodyStmt
    | RETURN expr? #return
    | BREAK #break
    | CONTINUE #continue
    ;

body: LBRACE bodyStmts* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
useStmt: USE STRING;
deferStmt: DEFER expr;

funcName
    : (extend_type=type DOT)? ID
    | op=(ADD | SUB | MUL | DIV | MOD | EEQ | NEQ | GT | LT | GTE | LTE | AND | OR | NOT)
    | (extend_type=type DOT)? NEW
    ;

funcAssign
    : STATIC? FUNC funcName LPAREN params? RPAREN (RETURNS return_type=type)? body
    ;
varAssign
    : ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | MUTABLE? ID ASSIGN expr
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
NEW: 'new';
USE: 'use';
FUNC: 'fn';
ELSE: 'else';
MUTABLE: 'mut';
DEFER: 'defer';
RETURN: 'return';
STATIC: 'static';

// Loop keywords
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: '"' .*? '"' | APOSTROPHE .*? APOSTROPHE;
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
RETURNS: '->';
AMPERSAND: '&';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
