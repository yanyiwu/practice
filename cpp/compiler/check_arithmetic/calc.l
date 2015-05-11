%{
#define YYSTYPE char*
#include "calc.tab.h"
#include "string.h"
#ifdef CALC_LEX
    YYSTYPE yylval;
#endif
%}

%%
"+"                                  { 
    fprintf(stderr, "%s", yytext);
    return ADD;    
} 
"-"                                  {
    fprintf(stderr, "%s", yytext);
    return SUB;    
} 
"*"                                  { 
    fprintf(stderr, "%s", yytext);
    return MUL;    
} 
"/"                                  { 
    fprintf(stderr, "%s", yytext);
    return DIV;    
} 
"("                                  { 
    fprintf(stderr, "%s", yytext);
    return OP;     
}
")"                                  { 
    fprintf(stderr, "%s", yytext);
    return CP;     
}
"{"                                  { 
    fprintf(stderr, "%s", yytext);
    return OPP;    
}
"}"                                  { 
    fprintf(stderr, "%s", yytext);
    return CPP;    
}
"|"                                  { 
    fprintf(stderr, "%s", yytext);
    return ABS;    
} 
"="                                  { 
    fprintf(stderr, "%s", yytext);
    return EQ;     
} 
([0-9]*\.?[0-9]+|[0-9]+\.[0-9]*)     { 
    fprintf(stderr, "%s", yytext);
    return NUMBER; 
} 
[a-zA-Z0-9]+                         { 
    fprintf(stderr, "%s", yytext);
    return WORD;   
}
\n                                   { 
    return EOL;    
} 
[ \t]                                { 
    /* ignore */   
} 

%%


#ifdef CALC_LEX  
int main (int argc, char** argv) {
    int token;


    while (token = yylex()) {
        printf("%d", token);


        if (token == NUMBER) {
            printf(" = %f\n", yylval);
        } else {
            printf("\n");
        }
    }


    return 0;
}
#endif 
