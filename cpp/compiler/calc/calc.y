/* simplest version of calculator */
%{
#include <stdio.h>
#define YYSTYPE double
%}
 /* declare tokens */
%token NUMBER 
%token ADD SUB MUL DIV ABS OP CP 
%token EOL 
%%
calclist: /* nothing */ 
 | calclist exp EOL { printf("= %f\n", $2); } 
 ;
exp: factor 
 | exp ADD factor { $$ = $1 + $3; }
 | exp SUB factor { $$ = $1 - $3; }
;
factor: term 
 | factor MUL term { $$ = $1 * $3; }
 | factor DIV term { $$ = $1 / $3; }
;
term: NUMBER 
 | ABS exp ABS { $$ = $2 >= 0? $2 : - $2; }
 | OP exp CP   { $$ = $2; }
;
%%
main(int argc, char **argv)
{
    yyparse();
}
yyerror(char *s)
{
    fprintf(stderr, "error: %s\n", s);
}
