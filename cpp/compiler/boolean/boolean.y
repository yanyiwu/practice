%token TRUE FALSE AND OR OP CP EOL
//%left AND

%%
exp:
        | exp boolexp EOL {printf("= %d\n", $2);}
        ;
boolexp: boolexp AND boolterm    {$$ = ($1 && $3);}
        | boolterm    {$$=$1;}
;

boolterm: OP boolexp CP {$$ = $2;}
        | bool  {$$ = $1;}
;

bool: TRUE {$$ = 1;}
    | FALSE {$$ = 0;}
;

%%
#include <stdio.h>

yyerror (char const *s) {
   fprintf (stderr, "%s\n", s);
}

int main(void) {
        yyparse();
}
