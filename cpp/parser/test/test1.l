%option noyywrap
%{
    int chars = 0;
    int words = 0;
    int lines = 0;
%}

%%
[a-zA-Z]+ {words++; chars += strlen(yytext);}
\n {}
. {}
%%

int main(int argc, char **argv) {
    while(yylex() != 0);
    printf("%d%d%d\n", lines, words, chars);
    return 0;
}
