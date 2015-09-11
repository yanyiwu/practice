%{
#include "boolean.tab.h"
%}

%%
"true"  {return TRUE;}
"false" {return FALSE;}
\n                                   { return EOL;    } 
"and"         {return AND;}
[()]           {return yytext[0];}

%%
