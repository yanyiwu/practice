#if !defined(_SHINGLE_H_)
#define _SHINGLE_H_

#include <stdio.h>
#include "html.h"
#include "fprint.h"
#include <iostream>
using namespace std;

struct shingle_s;

typedef struct shingle_s *shingle_t;

shingle_t shingle_new (unsigned windowsize, unsigned nminima);
/* return a new shingle_t suitable for shingling documents.
   "windowsize" is the shingling window to be slid across the doucment.
   "nminima" is the total number of fingerprints to be calculated at each window position */

void processword (void *v, unsigned char *w, int len);
void zapstrings (shingle_t s);

void shingle_stream (shingle_t s, int (*getch) (void *), void *f, fprint_t minima[]);
/* Parse the document readable on stream "f", where the getch
   function returns the next character of the stream, and shingle it,
   leaving the resulting fingerprints in "minima[0, ..., nminima-1]". */

void shingle_doc (shingle_t s, FILE *fp, fprint_t minima[]);
/* Parse the document readable on stdio stream "fp" and shingle it,
   leaving the resulting fingerprints in "minima[0, ..., nminima-1]". */

void shingle_supershingle (shingle_t s, fprint_t minima[], fprint_t supershingles[], unsigned nsupershingles);
/* Deterministically divide the "nminima" fingerprints in
   "minima" into "nsupershingles" equal-sized non-overlapping
   groups (or as close to equal-sized as possible),
   and fingerprint each group, leaving the results in
   "supershingles[0, ..., nsupershingles-1]" */

void shingle_megashingle (shingle_t s, fprint_t supershingles[], unsigned nsupershingles,
	fprint_t megashingles[], unsigned choose);
/* Form N=("nsupershingles" choose "choose") tuples of fingerprints from the list in 
   "supershingles[0, ..., nsupershingles-1]".   Fingerprint each tuple and place the
   resulting fingerprints in "megashingles[0, ..., N-1]". */

void shingle_destroy (shingle_t s);
/* destroy an existing shingle_t */

#endif
