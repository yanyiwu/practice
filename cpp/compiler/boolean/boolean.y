//%token BOOL AND
//%left AND
//
//%%
//boolexp: boolexp AND boolterm    {$$ = !($1 && $3);}
//               | boolterm    {$$=$1;}
//               ;
//
//boolterm: '(' boolexp ')'
//                | BOOL  {$$ = (strcmp($1, "true")) ? 1 : 0;} 
//                ;
//
//%%
//#include <lex.yy.c>
//
//int main(void) {
//        yyparse();
//}


%token TRUE FALSE AND
%left AND
%token EOL 

%%
exp:
        | exp boolexp EOL {printf("= %d\n", $2);}
        ;
boolexp: boolexp AND boolterm    {$$ = ($1 && $3);}
        | boolterm    {$$=$1;}
;

boolterm: '(' boolexp ')' {$$ = $2;}
        | bool  {$$ = $1;}
;

bool: TRUE {$$ = 1;}
    | FALSE {$$ = 0;}
;

%%
#include <stdio.h>

void yyerror (char const *s) {
   fprintf (stderr, "%s\n", s);
}

int main(void) {
        yyparse();
}
