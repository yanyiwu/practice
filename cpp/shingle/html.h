#if !defined(_HTML_H_)
#define _HTML_H_
#include <stdlib.h>
#include "mi_ctype8.h"
#include <string.h>

void html_parse (int (*getch) (void *), void *iv, void (*putword) (void *, unsigned char *, int), void *ov);
/* Call (*getch) (iv) repeatedly to get the characters of some HTML text.
   Ignore tags, and call (*putword) (ov, word, len) on each maximal sequence of alphanumeric
   characters in the text returned via "getch".  The string "word" is null-terminated,
   and contains "len" > 1 non-null characters.  

   Assumes that (*getch) (iv) will return the 8-bit characters of the inout, in order,
   and then return -1.
*/

#endif
