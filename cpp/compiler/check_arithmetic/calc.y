/* simplest version of calculator */
%{
#include <stdio.h>
#include <stdlib.h>
#define YYSTYPE char*
%}
 /* declare tokens */
%token NUMBER 
%token WORD
%token ADD SUB MUL DIV ABS OP CP EQ OPP CPP
%token EOL 

%%
program: /* nothing */ 
 | program exp EOL { fprintf(stderr, "\n"); } 
 | program error EOL {fprintf(stderr, "ERROR\n");}
;
exp: factor 
 | exp ADD factor { $$ = 0; }
 | exp SUB factor { $$ = 0; }
;
factor: term 
 | factor MUL term { $$ = 0; }
 | factor DIV term { $$ = 0; }
 | factor EQ term  { $$ = 0; }
;
term: NUMBER
 | WORD        
 | ABS exp ABS { $$ = 0; }
 | OP exp CP   { $$ = 0; }
 | OPP exp CPP { $$ = 0; }
;
%%
main(int argc, char **argv)
{
    yyparse();
}
yyerror(char *s)
{
    //fprintf(stderr, "error: %s\n", s);
}
