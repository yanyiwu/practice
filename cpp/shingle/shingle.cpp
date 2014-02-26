#include <stdlib.h>
#include <string.h>

#include "shingle.h"

#if defined(XSHINGLE_TEST)
#undef malloc
#undef free
void *mi_malloc_X (size_t n, char *file, int line);
void mi_free_X (void *p, char *file, int line);
#define malloc(_n) mi_malloc_X(_n, __FILE__, __LINE__)
#define free(_p) mi_free_X(_p, __FILE__, __LINE__)
#endif



static unsigned char *stralloc (unsigned char *s) {
	char *p = (char *)malloc (strlen ((const char*)s) + 1);
	return (unsigned char*)(strcpy (p, (const char*)s));
}

static unsigned char *cat (unsigned char *a[], int start, int count) {
	int i;
	int l = 0;
	unsigned char *p;
	for (i = 0; i != count; i++) {
		l += strlen ((const char *)a[i]) + 1;
	}
	p = (unsigned char*)malloc (l+1);
	p[0] = 0;
	i = start;
	do {
		strcat ((char*)p, (char*)a[i]);
		strcat ((char*)p, " ");
		i++;
		if (i == count) {
			i = 0;
		}
	} while (i != start);
	return (p);
}

void processword (void *v, unsigned char *w, int len);

struct shingle_s {
	fprint_uint64_t *first;		/* array size windowsize-1 */
	unsigned char **first_strings; 	/* array size windowsize-1 */
	fprint_uint64_t *window; 	/* array size windowsize */
	unsigned char **win_strings; 	/* array size windowsize */
	unsigned nminima;
	unsigned windowsize;
	int i;
	int i_mod;
	fprint_data_t fp_word;
	fprint_data_t fp_ss;
	fprint_data_t fp_ms;
	fprint_data_t *fp_shingle;	/* array size nminima */
	fprint_t *current;		/* array size nminima */
	fprint_t *minima;		/* array size nminima */
	unsigned char **min_strings;	/* array size nminima */
};

void processword (void *v, unsigned char *w, int len) {
	shingle_t s = (shingle_t)v;
	fprint_t fw = fprint_extend (s->fp_word, fprint_empty (s->fp_word), w, len);
	if (s->i < s->windowsize) {
		s->window[s->i_mod] = fw;
#if defined(SHINGLE_TEST)
		s->win_strings[s->i_mod] = stralloc (w);
#endif
		if (s->i == s->windowsize-1) {
			int m;
#if defined(SHINGLE_TEST)
			unsigned char *best = cat (s->win_strings, 0, s->windowsize);
#endif
			for (m = 0; m != s->nminima; m++) {
				s->current[m] = fprint_extend_word (s->fp_shingle[m],
					fprint_empty (s->fp_shingle[m]), s->window, s->windowsize);
				s->minima[m] = s->current[m];
#if defined(SHINGLE_TEST)
				s->min_strings[m] = stralloc (best);
#endif
			}
#if defined(SHINGLE_TEST)
			free (best);
#endif
		} else {
			s->first[s->i] = fw;
			s->first_strings[s->i] = stralloc (w);
		}
	} else {
		int m;
#if defined(SHINGLE_TEST)
		free (s->win_strings[s->i_mod]);
		s->win_strings[s->i_mod] = stralloc (w);
#endif
		for (m = 0; m != s->nminima; m++) {
			s->current[m] = fprint_slideword (s->fp_shingle[m], s->current[m],
				s->window[s->i_mod], fw);
			if (s->current[m] < s->minima[m]) {
				s->minima[m] = s->current[m];
#if defined(SHINGLE_TEST)
				free (s->min_strings[m]);
				s->min_strings[m] = cat (s->win_strings, (s->i_mod+1) % s->windowsize, s->windowsize);
#endif
			}
		}
		s->window[s->i_mod] = fw;
	}
	s->i++;
	s->i_mod++;
	if (s->i_mod == s->windowsize) {
		s->i_mod = 0;
	}
}

shingle_t shingle_new (unsigned windowsize, unsigned nminima) {
	shingle_t s = (shingle_t)malloc (sizeof (*s));
	int fi = 0;
	int i;
	memset (s, 0, sizeof (*s));
	s->nminima = nminima;
	s->windowsize = windowsize;
	s->first = (fprint_uint64_t *)malloc (sizeof (s->first[0]) * (s->windowsize-1));
	s->first_strings = (unsigned char**)malloc (sizeof (s->first_strings[0]) * (s->windowsize-1)); 
	memset (s->first_strings, 0, sizeof (s->first_strings[0]) * (s->windowsize-1));
	s->window = (fprint_uint64_t *)malloc (sizeof (s->window[0]) * s->windowsize); 
	s->win_strings = (unsigned char**)malloc (sizeof (s->win_strings[0]) * s->windowsize); 
	memset (s->win_strings, 0, sizeof (s->win_strings[0]) * s->windowsize);
	s->fp_shingle = (fprint_data_t*)malloc (sizeof (s->fp_shingle[0]) * s->nminima);
	s->current = (fprint_t*)malloc (sizeof (s->current[0]) * s->nminima);
	s->minima = (fprint_t *)malloc (sizeof (s->minima[0]) * s->nminima);
	s->min_strings = (unsigned char **)malloc (sizeof (s->min_strings[0]) * s->nminima);
	memset (s->min_strings, 0, sizeof (s->min_strings[0]) * s->nminima);
	s->fp_word = fprint_new (fprint_polys[fi++], 0);
	s->fp_ss = fprint_new (fprint_polys[fi++], 0);
	for (i = 0; i != s->nminima; i++) {
		s->fp_shingle[i] = fprint_new (fprint_polys[fi++], s->windowsize);
	}
	s->fp_ms = fprint_new (fprint_polys[fi++], 0);
	return (s);
}

void zapstrings (shingle_t s) {
	int i;
	for (i = 0; i != s->windowsize-1; i++) {
		if (s->first_strings[i] != 0) {
			free (s->first_strings[i]);
			s->first_strings[i] = 0;
		}
	}
	for (i = 0; i != s->windowsize; i++) {
		if (s->win_strings[i] != 0) {
			free (s->win_strings[i]);
			s->win_strings[i] = 0;
		}
	}
	for (i = 0; i != s->nminima; i++) {
		if (s->min_strings[i] != 0) {
			free (s->min_strings[i]);
			s->min_strings[i] = 0;
		}
	}
	s->i = 0;
	s->i_mod = 0;
}

void shingle_stream (shingle_t s, int (*getch) (void *), void *f, fprint_t minima[]) {
	int i;
	zapstrings (s);
	html_parse (getch, f, processword, s);
	if (s->i != 0) {
		for (i = 0; i != s->windowsize-1; i++) {
			processword (s, s->first_strings[i], strlen ((const char*)s->first_strings[i]));
		}
	}
	memcpy (minima, s->minima, sizeof (minima[0]) * s->nminima);
}

void shingle_doc (shingle_t s, FILE *fp, fprint_t minima[]) {
	int i;
	zapstrings (s);
	html_parse ((int (*) (void *)) fgetc, fp, processword, s);
	if (s->i != 0) {
		for (i = 0; i != s->windowsize-1; i++) {
			processword (s, s->first_strings[i], strlen ((const char *)s->first_strings[i]));
		}
	}
	memcpy (minima, s->minima, sizeof (minima[0]) * s->nminima);
}

void shingle_supershingle (shingle_t s, fprint_t minima[],
	fprint_t supershingles[], unsigned nsupershingles) {
		unsigned i;
		int j;
		int nj;
		for (i = 0, j = 0; i != nsupershingles; i++, j = nj) {
			nj = (s->nminima * (i+1)) / nsupershingles;
			supershingles[i] = fprint_extend_word (s->fp_ss, fprint_empty (s->fp_ss), 
				&minima[j], nj-j);
		/*	{
				int h;
				for (h = j; h != nj; h++) {
					fprint_output ((void (*) (int, void *)) fputc, stdout, minima[h]);
					printf (" ");
				}
				printf ("\n");
			}*/
		}
}

static fprint_t *megashingle (shingle_t s, fprint_t supershingles[], unsigned nsupershingles,
	fprint_t megashingles[], unsigned choose, unsigned i, fprint_t *buf) {
		int j;
		for (j = 0; j != nsupershingles; j++) {
			buf[i] = supershingles[j];
			if (i+1 < choose) {
				megashingles = megashingle (s, &supershingles[j+1], nsupershingles-j-1,
					megashingles, choose, i+1, buf);
			} else {
				*megashingles++ = fprint_extend_word (s->fp_ms, fprint_empty (s->fp_ms),
					buf, choose);
				{
					int h;
					for (h = 0; h != choose; h++) {
						fprint_output ((void (*) (int, void *)) fputc, stdout, buf[h]);
						printf (" ");
					}
					printf ("\n");
				}
			}
		}
		return (megashingles);
}

void shingle_megashingle (shingle_t s, fprint_t supershingles[], unsigned nsupershingles,
	fprint_t megashingles[], unsigned choose) {
		fprint_t *buf = (fprint_t *)malloc (sizeof (buf[0]) * choose);
		fprint_t *em = megashingle (s, supershingles, nsupershingles, megashingles, choose, 0, buf);
		printf ("%d\n", em-megashingles);
		free (buf);
}

void shingle_destroy (shingle_t s) {
	int i;
	zapstrings (s);
	for (i = 0; i != s->nminima; i++) {
		fprint_close (s->fp_shingle[i]);
	}
	free (s->current);
	free (s->minima);
	free (s->min_strings);
	fprint_close (s->fp_word);
	fprint_close (s->fp_ss);
	fprint_close (s->fp_ms);
	free (s->fp_shingle);
	free (s->first);
	free (s->first_strings);
	free (s->window);
	free (s->win_strings);
	free (s);
}

#if defined(SHINGLE_TEST)
#include <stdio.h>
#include <ctype.h>
#include <sys/file.h>
#if defined(__CYGWIN__)
#include <io.h>
#endif

static char *prog;
void usage (void) {
	printf (stderr, "usage: %s [-w window] [-m minima] [-s nsupershingles] [-c choose]\n", prog);
	exit (2);
}

int main (int argc, char *argv[]) {
	int argn;
	int i;
	int rc = 0;
	int noflags = 0;
	FILE *ifp;
	FILE *ofp;
	shingle_t s;
	unsigned windowsize = 6;
	unsigned nminima = 24;
	unsigned nsupershingles = 6;
	unsigned choose = 2;
	unsigned nmegashingles;
	fprint_t *minima; /* array size nminima */
	fprint_t *supershingles;	/* array size nsupershingles */
	fprint_t *megashingles;		/* array size nmegashingles */
	if ((prog = strrchr (argv[0], '/')) == 0) {
		prog = argv[0];
	} else {
		prog++;
	}
	for (argn = 1; argn < argc; argn++) {
		if (argv[argn][0] == '-' && noflags==0 && argv[argn][1]!=0) {
			char *f = &argv[argn][1];
			while (*f != 0) {
				switch (*f) {
				case 'e':
					noflags = 1;
					break;
				case 'c':
					if (argn+1 >= argc) { usage (); }
					choose = atoi (argv[++argn]);
					break;
				case 'm':
					if (argn+1 >= argc) { usage (); }
					nminima = atoi (argv[++argn]);
					break;
				case 's':
					if (argn+1 >= argc) { usage (); }
					nsupershingles = atoi (argv[++argn]);
					break;
				case 'w':
					if (argn+1 >= argc) { usage (); }
					windowsize = atoi (argv[++argn]);
					break;
				default: usage (); break;
				}
				f++;
			}
		} else {
			usage ();
		}
	}
#if defined(xx__CYGWIN__)
	setmode (0, O_BINARY);
	setmode (1, O_BINARY);
#endif
	ifp = stdin;
	ofp = stdout;

	nmegashingles = 1;
	for (i = 0; i != choose; i++) {
		nmegashingles *= nsupershingles-i;
		nmegashingles /= i+1;
	}

	minima = malloc (sizeof (minima[0]) * nminima);
	supershingles = malloc (sizeof (supershingles[0]) * nsupershingles);
	megashingles = malloc (sizeof (megashingles[0]) * nmegashingles);

	s = shingle_new (windowsize, nminima);

	shingle_doc (s, ifp, minima);

	for (i = 0; i != nminima; i++) {
		printf ("sh %03d ", i);
		fprint_output ((void (*) (int, void *)) fputc, ofp, minima[i]);
		printf (" %s\n", s->min_strings[i]);
	}
	printf ("\n");

	shingle_supershingle (s, minima, supershingles, nsupershingles);
	for (i = 0; i != nsupershingles; i++) {
		printf ("ss %03d ", i);
		fprint_output ((void (*) (int, void *)) fputc, ofp, supershingles[i]);
		printf ("\n");
	}
	printf ("\n");

	shingle_megashingle (s, supershingles, nsupershingles, megashingles, choose);
	for (i = 0; i != nmegashingles; i++) {
		printf ("ms %03d ", i);
		fprint_output ((void (*) (int, void *)) fputc, ofp, megashingles[i]);
		printf ("\n");
	}

	shingle_destroy (s);

	free (minima);
	free (supershingles);
	free (megashingles);

	if (ferror (ifp)) {
		perror ("input");
		rc = 2;
	}
	fflush (ofp);
	if (ferror (ofp)) {
		perror ("output");
		rc = 2;
	}
	return (rc);
}
#endif

