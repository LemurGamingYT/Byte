grammar Byte;

program: stmt* EOF;

type: ID;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt | useStmt | deferStmt
    | expr
    ;

bodyStmts
    : stmt #bodyStmt
    | RETURN expr #return
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

func_name
    : extend_type=type DOT ID
    | ID
    | op=(ADD | SUB | MUL | DIV | MOD | EEQ | NEQ | GT | LT | GTE | LTE | AND | OR | NOT)
    ;

funcAssign
    : STATIC? FUNC func_name LPAREN params? RPAREN (RETURNS return_type=type)? body
    ;
varAssign
    : ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | MUTABLE? ID ASSIGN expr
    ;

arg: expr;
args: arg (COMMA arg)*;

param: MUTABLE? type ID;
params: param (COMMA param)*;

expr
    : ID LPAREN args? RPAREN #call
    | LPAREN expr RPAREN #paren
    | INT #int
    | FLOAT #float
    | STRING #string
    | BOOL #bool
    | ID #id
    | expr IF expr ELSE expr #ternary
    | expr DOT ID (LPAREN args? RPAREN)? #attr
    | expr op=(MUL | DIV | MOD) expr #multiplication
    | expr op=(ADD | SUB) expr #addition
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr #relational
    | expr op=(AND | OR) expr #logical
    | op=(NOT | SUB | ADD) expr #unary
    ;


// Basic keywords
IF: 'if';
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

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
