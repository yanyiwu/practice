%{
#include "boolean.tab.h"
%}

%%
"true"  {return TRUE;}
"false" {return FALSE;}
"and"   {return AND;}
"or"   {return OR;}
"("     {return OP;}
")"     {return CP;}
\n      {return EOL;} 

%%
