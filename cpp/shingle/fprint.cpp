#include <stdlib.h>

#include "fprint.h"

#if defined(FPRINT_TEST) || defined(XSHINGLE_TEST)
#include <stdio.h>
extern void pfp (fprint_t);
#if defined(MIKES_WORLD)
#undef malloc
#undef free
void *mi_malloc_X (size_t n, char *file, int line);
void mi_free_X (void *p, char *file, int line);
#define malloc(_n) mi_malloc_X(_n, __FILE__, __LINE__)
#define free(_p) mi_free_X(_p, __FILE__, __LINE__)
#endif
#endif

#define BYTESWAP_FP(_x) \
	( \
	((_x) << 56) | \
	((_x) >> 56) | \
	(((_x) & 0x0000ff00UL) << 40) | \
	(((_x) >> 40) & 0x0000ff00UL) | \
	(((_x) & 0x00ff0000UL) << 24) | \
	(((_x) >> 24) & 0x00ff0000UL) | \
	(((_x) & 0xff000000UL) << 8) | \
	(((_x) >> 8) & 0xff000000UL) \
	)

struct fprint_data_s {
	fprint_t poly[2];		/* poly[0] = 0; poly[1] = polynomial */
	fprint_t empty;			/* fingerprint of the empty string */
	fprint_t bybyte[8][256];	/* bybyte[b][i] is i*X^(64+8*b) mod poly[1] */
	fprint_t bybyte_r[8][256];	/* bybyte[b][i] is i*X^(64+8*b) mod poly[1],
								byte-swapped */
	fprint_t powers[64];		/* extend[i] is X^(8*2^i) mod poly[1] */
#define LOGZEROBLOCK 8
#define ZEROBLOCK (1 << LOGZEROBLOCK)
	union {
		double align;
		unsigned char zeroes[ZEROBLOCK];
	} zeroes;
	fprint_t bybyte_out[8][256];	/* bybyte[b][i] is i*X^(64+8*(b+span)) mod poly[1] */
	unsigned span;
};

static void initbybyte (fprint_data_t fp, fprint_t bybyte[][256], fprint_t f) {
	int b;
	for (b = 0; b != 8; b++) {
		int i;
		bybyte[b][0] = 0;
		for (i = 0x80; i != 0; i >>= 1) {
			bybyte[b][i] = f;
			f = fp->poly[f & 1] ^ (f >> 1);
		}
		for (i = 1; i != 256; i <<= 1) {
			fprint_t xf = bybyte[b][i];
			int k;
			for (k = 1; k != i; k++) {
				bybyte[b][i+k] = xf ^ bybyte[b][k];
			}
		}
	}
}

void fprint_init(fprint_data_t fp, fprint_t poly, unsigned span) {
	fprint_t l;
	int i, j;
	fp->poly[0] = 0;
	fp->poly[1] = poly;	/*This must be initialized early on */
	fp->empty = poly;
	fp->span = span;
	initbybyte (fp, fp->bybyte, poly); /* bybyte[][] must be initialized before powers[] */
	for (i = 0; i < 8; i++)
		for (j = 0; j < 256; j++)
			fp->bybyte_r[i][j] = BYTESWAP_FP(fp->bybyte[i][j]);
	memset (&fp->zeroes, 0, sizeof (fp->zeroes)); /* zeroes must be initialized before powers[] */
	/* The initialization of powers[] must happen after bybyte[][] and zeroes
	are initialized because concat uses all of bybyte[][], zeroes
	and the prefix of powers[] internally.  */
	fp->powers[0] = ((fprint_t) 1) << 55;
	for (i = 1, l = 1; i != sizeof (fp->powers) / sizeof (fp->powers[0]); i++, l <<= 1) {
		fp->powers[i] = fprint_concat (fp, fp->powers[i-1] ^ poly, 0, l);
	}
	if (span != 0) {
		initbybyte (fp, fp->bybyte_out, fprint_concat (fp, 0, 0, (span-1) * 8));
	}
}

fprint_data_t fprint_new (fprint_t poly, unsigned span) {
	fprint_data_t fp = (fprint_data_t)malloc (sizeof (*fp));
	fprint_init(fp, poly, span);
	return fp;
}

fprint_t fprint_empty (fprint_data_t fp) {
	return (fp->empty);
}

fprint_t fprint_slideword (fprint_data_t fp, fprint_t f, fprint_uint64_t a, fprint_uint64_t b) {
	a ^= fp->poly[1] ^ (((fprint_t) 1) << 63);
	f ^=fp->bybyte_out[7][a & 0xff] ^
		fp->bybyte_out[6][(a >> 8) & 0xff] ^
		fp->bybyte_out[5][(a >> 16) & 0xff] ^
		fp->bybyte_out[4][(a >> 24) & 0xff] ^
		fp->bybyte_out[3][(a >> 32) & 0xff] ^
		fp->bybyte_out[2][(a >> 40) & 0xff] ^
		fp->bybyte_out[1][(a >> 48) & 0xff] ^
		fp->bybyte_out[0][a >> 56];
	f ^= b;
	f = fp->bybyte[7][f & 0xff] ^
		fp->bybyte[6][(f >> 8) & 0xff] ^
		fp->bybyte[5][(f >> 16) & 0xff] ^
		fp->bybyte[4][(f >> 24) & 0xff] ^
		fp->bybyte[3][(f >> 32) & 0xff] ^
		fp->bybyte[2][(f >> 40) & 0xff] ^
		fp->bybyte[1][(f >> 48) & 0xff] ^
		fp->bybyte[0][f >> 56];
	return (f);
}

fprint_t fprint_extend_word (fprint_data_t fp, fprint_t init, fprint_uint64_t *data, unsigned len) {
	unsigned i;
	for (i = 0; i != len; i++) {
		init ^= data[i];
		init =  fp->bybyte[7][init & 0xff] ^
			fp->bybyte[6][(init >> 8) & 0xff] ^
			fp->bybyte[5][(init >> 16) & 0xff] ^
			fp->bybyte[4][(init >> 24) & 0xff] ^
			fp->bybyte[3][(init >> 32) & 0xff] ^
			fp->bybyte[2][(init >> 40) & 0xff] ^
			fp->bybyte[1][(init >> 48) & 0xff] ^
			fp->bybyte[0][init >> 56];
	}
	return (init);
}

fprint_t fprint_extend (fprint_data_t fp, fprint_t init, void *data, unsigned len) {
	unsigned char *p = (unsigned char *)data;
	unsigned char *e = p+len;
	while (p != e && (((long) p) & 7L) != 0) {
		init = (init >> 8) ^ fp->bybyte[0][(init & 0xff) ^ *p++];
	}
	if (ENDIAN_LITTLE) {
		while (p+8 <= e) {
			init ^= *(fprint_t *)p;
			init =  fp->bybyte[7][init & 0xff] ^
				fp->bybyte[6][(init >> 8) & 0xff] ^
				fp->bybyte[5][(init >> 16) & 0xff] ^
				fp->bybyte[4][(init >> 24) & 0xff] ^
				fp->bybyte[3][(init >> 32) & 0xff] ^
				fp->bybyte[2][(init >> 40) & 0xff] ^
				fp->bybyte[1][(init >> 48) & 0xff] ^
				fp->bybyte[0][init >> 56];
			p += 8;
		}
	} else if (p + 8 <= e) {
		init = BYTESWAP_FP (init);
		while (p+16 <= e) {
			init ^= *(fprint_t *)p;
			init =  fp->bybyte_r[0][init & 0xff] ^
				fp->bybyte_r[1][(init >> 8) & 0xff] ^
				fp->bybyte_r[2][(init >> 16) & 0xff] ^
				fp->bybyte_r[3][(init >> 24) & 0xff] ^
				fp->bybyte_r[4][(init >> 32) & 0xff] ^
				fp->bybyte_r[5][(init >> 40) & 0xff] ^
				fp->bybyte_r[6][(init >> 48) & 0xff] ^
				fp->bybyte_r[7][init >> 56];
			p += 8;
		}
		init ^= *(fprint_t *)p;
		init =  fp->bybyte[0][init & 0xff] ^
			fp->bybyte[1][(init >> 8) & 0xff] ^
			fp->bybyte[2][(init >> 16) & 0xff] ^
			fp->bybyte[3][(init >> 24) & 0xff] ^
			fp->bybyte[4][(init >> 32) & 0xff] ^
			fp->bybyte[5][(init >> 40) & 0xff] ^
			fp->bybyte[6][(init >> 48) & 0xff] ^
			fp->bybyte[7][init >> 56];
		p += 8;
	}

	while (p != e) {
		init = (init >> 8) ^ fp->bybyte[0][(init & 0xff) ^ *p++];
	}
	return (init);
}


fprint_t fprint_concat (fprint_data_t fp, fprint_t a, fprint_t b, fprint_t blen) {
	int i;
	fprint_t x = blen;
	unsigned low = x & ((1 << LOGZEROBLOCK)-1);
	a ^= fp->poly[1];
	if (low != 0) {
		a = fprint_extend (fp, a, fp->zeroes.zeroes, low);
	}
	x >>= LOGZEROBLOCK;
	i = LOGZEROBLOCK;
	while (x != 0) {
		if (x & 1) {
			fprint_t m = 0;
			fprint_t bit;
			fprint_t e = fp->powers[i];
			for (bit = ((fprint_t) 1) << 63; bit != 0; bit >>= 1) {
				if (e & bit) {
					m ^= a;
				}
				a = (a >> 1) ^ fp->poly[a & 1];
			}
			a = m;
		}
		x >>= 1;
		i++;
	}
	return (a ^ b);
}

void fprint_output (void (*outc) (int c, void *v), void *v, fprint_t f) {
	int i;
	for (i = 60; i != -4; i -= 4) {
		(*outc) ("0123456789abcdef"[(f >> i) & 0xf], v);
	}
}

void fprint_toascii (fprint_t f, char *buf) {
	int i;
	for (i = 60; i != -4; i -= 4) {
		*buf++ = "0123456789abcdef"[(f >> i) & 0xf];
	}
}


void fprint_close (fprint_data_t fp) {
	free (fp);
}

fprint_t mul(fprint_data_t fp, fprint_t a, fprint_t b) {
	fprint_t res = 0L;
	while (b) {
		if (b & ((fprint_t) 1) << 63) {
			res ^= a;
		}
		a = (a >> 1) ^ fp->poly[a & 1];
		b <<= 1;
	}
	return res;
}

/* This is faster, if you've already built a full struct */
fprint_t pow2(fprint_data_t fp, fprint_t power) {
	fprint_t one = fp->poly[1] ^ (((fprint_t)1L) << (63 - (power % 8)));
	fprint_t pow8 = power / 8;
	return fprint_concat(fp, one, 0, pow8);
}

fprint_t pow(fprint_data_t fp, fprint_t power) {
	fprint_t res;
	if (power <= 1)
		return ((fprint_t)1) << (63 - power);
	res = pow(fp, power >> 1);
	res = mul(fp, res, res);
	if (power & 1)
		return mul(fp, res, ((fprint_t)1) << 62);
	else
		return res;
}

const int factors[] = {3, 5, 17, 257, 641, 6637, 6700417L};
#define nfactors (sizeof(factors) / sizeof(factors[0]))

/* Check polynomial for primitivity.  Return 1 if so, 0 otherwise. */
int test_poly(fprint_t p, int noisy) {
	static fprint_data_t fp = 0;
	static fprint_t order = ~((fprint_t) 0);
	static fprint_t div[nfactors];
	fprint_t one = ((fprint_t) 1) << 63;
	int i;
	if (fp) {
		/* do this to use pow2 */
		/* fprint_init(fp, p, 0); */
		fp->poly[1]= p;
	} else {
		for (i = 0; i < nfactors; i++)
			div[i] = order / factors[i];
		/* do this to use pow2 */
		/* fp = fprint_new(p, 0); */
		fp = (fprint_data_t)malloc (sizeof (*fp));
		fp->poly[0] = 0;
		fp->poly[1] = p;
	}
	if (( pow(fp, order)) != one ) {
#if defined(FPRINT_TEST) || defined(XSHINGLE_TEST)
		if (noisy) {
			printf("Little Fermat failed on "); pfp(p);
			printf(" -> "); pfp(pow2(fp, order)); printf("\n");
		}
#endif
		return 0;
	}
	for (i = 0; i < nfactors; i++) {
		if (( pow(fp, div[i])) == one ) {
#if defined(FPRINT_TEST) || defined(XSHINGLE_TEST)
			if (noisy) {
				printf("Order test failed on ");
				pfp(p);
				printf(" for divisor %d\n", factors[i]);
			}
#endif
			return 0;
		}
	}
	return 1;
}

/* (((fprint_t) 0x911498aeUL) << 32) | (fprint_t) 0x0e66bad6UL,  /* Andrei's polynomial */
const fprint_t fprint_polys[] = {
#include "polynomials.h"
};
const int fprint_npolys = sizeof (fprint_polys) / sizeof (fprint_polys[0]);

//#define  FPRINT_TEST 1

#if defined(FPRINT_TEST)
#include <stdio.h>
#include <string.h>

void pfp (fprint_t f) {
	fprint_output ((void (*) (int, void *)) fputc, stdout, f);
}

fprint_t fprint_extend_string (fprint_data_t fp, fprint_t f, char *str) {
	return (fprint_extend (fp, f, str, strlen (str)));
}
fprint_t fprint_string (fprint_data_t fp, char *str) {
	return (fprint_extend (fp, fp->empty, str, strlen (str)));
}

fprint_t fprint_extend_bybit (fprint_data_t fp, fprint_t init, void *data, unsigned len) {
	unsigned char *p = (unsigned char *)data;
	unsigned char *e = p+len;
	while (p != e) {
		int i;
		int b = *p++;
		for (i = 0; i != 8; i++) {
			init = (init >> 1) ^ fp->poly[(init ^ b) & 1];
			b >>= 1;
		}
	}
	return (init);
}
fprint_t fprint_extend_bybyte (fprint_data_t fp, fprint_t init, void *data, unsigned len) {
	unsigned char *p = (unsigned char *)data;
	unsigned char *e = p+len;
	while (p != e) {
		init = (init >> 8) ^ fp->bybyte[0][(init & 0xff) ^ *p++];
	}
	return (init);
}

int main (int argc, char *argv[]) {
	int p;
	int i, j;
#define NUMKB 128
#define BSIZ (NUMKB*1024)
	unsigned char *buf = (unsigned char *)malloc (BSIZ);
	char fpc[] = "(fprint_t) ";
	fprint_t fp;
	if (fprint_npolys < 200) {
		FILE *polyfile = fopen("polynomials.h", "w");
		FILE *pfile2 = fopen("polys.cs", "w");
		fprintf(pfile2, "using UInt64 = System.UInt64;\n");
		fprintf(pfile2, "  namespace Shingle {\nstruct Polynomials {\n");
		fprintf(pfile2, "    public static readonly UInt64[] polys = {\n");

		srand(/*(unsigned long)time(NULL)*/1024);
		for (i = 0; i < 200; ) {
			for (j = 0, fp = 0; j < 8; j++) {
				fp = (fp << 8) | (0xff & rand());
			}
			fp |= ((fprint_t)1) << 63;
			if (test_poly(fp,0)) {
				if (i != 0) {
					fprintf(polyfile, ",\n");
					fprintf(pfile2, ",\n");
				}
				fprintf(polyfile,
					"/* %03d */\t((%s0x%08xUL) << 32) | ",
					i++, fpc, fp >> 32);
				fprintf(polyfile, "%s0x%08xUL", fpc, fp & 0xffffffffUL);
				fprintf(pfile2, "/* %03d */\t0x%08x",
					i - 1, fp >> 32);
				fprintf(pfile2, "%08xUL", fp & 0xffffffffUL);
			}
		}
		fprintf(polyfile, "\n");
		fclose(polyfile);
		fprintf(pfile2, "\n    };\n  }\n}");
		fclose(pfile2);
		printf("Wrote polynomials.h and polys.cs with new, personal polynomials.\nRecompile!\n");
		exit(0);
	}
	for (i = 0; i < fprint_npolys; i++) {
		printf("Testing polynomial %d for primitivity\n", i);
		test_poly(fprint_polys[i], 1);
	}
	for (i = 0; i != BSIZ; i++) {
		buf[i] = rand();
	}
	for (p = 0; p != 1; p++) {
		fprint_data_t fp = fprint_new (fprint_polys[p], 3);
		fprint_t f;
		fprint_t a2l;
		fprint_t m2z;
		fprint_t a2z;
		fprint_t a2za2z;
		fprint_uint64_t w[6];
		int i;
		int j;
		int k;
		int l;
		fprint_t s;
		for (i = 0; i != sizeof (w) / sizeof (w[0]); i++) {
			w[i] = rand () ^ (((fprint_uint64_t) rand()) << 11) ^ (((fprint_uint64_t) rand()) << 33);
		}
		printf ("polynomial           = "); pfp (fprint_polys[p]); printf ("\n");
		printf ("empty                = "); pfp (fprint_empty (fp)); printf ("\n");
		printf ("fprint(\"\")           = "); pfp (fprint_string (fp, "")); printf ("\n");
		printf ("\n");
		printf ("fprint(\"^@\") normal  = "); pfp (fprint_extend (fp, fprint_empty (fp), "", 1)); printf ("\n");
		printf ("fprint(\"^@\") bytes   = "); pfp (fprint_extend_bybyte (fp, fprint_empty (fp), "", 1)); printf ("\n");
		printf ("fprint(\"^@\") bits    = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), "", 1)); printf ("\n");
		printf ("\n");
		printf ("fprint(\"a\") normal   = "); pfp (fprint_extend (fp, fprint_empty (fp), "a", 1)); printf ("\n");
		printf ("fprint(\"a\") bytes    = "); pfp (fprint_extend_bybyte (fp, fprint_empty (fp), "a", 1)); printf ("\n");
		printf ("fprint(\"a\") bits     = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), "a", 1)); printf ("\n");
		printf ("\n");
		printf ("fprint(\"a...l\")normal= "); pfp (a2l = fprint_extend (fp, fprint_empty (fp), "abcdefghijkl", 12)); printf ("\n");
		printf ("fprint(\"a...l\") bytes= "); pfp (fprint_extend_bybyte (fp, fprint_empty (fp), "abcdefghijkl", 12)); printf ("\n");
		printf ("fprint(\"a...l\") bits = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), "abcdefghijkl", 12)); printf ("\n");
		printf ("\n");
		printf ("fprint(\"m...z\")normal= "); pfp (m2z = fprint_extend (fp, fprint_empty (fp), "mnopqrstuvwxyz", 14)); printf ("\n");
		printf ("fprint(\"m...z\") bytes= "); pfp (fprint_extend_bybyte (fp, fprint_empty (fp), "mnopqrstuvwxyz", 14)); printf ("\n");
		printf ("fprint(\"m...z\") bits = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), "mnopqrstuvwxyz", 14)); printf ("\n");
		printf ("\n");
		printf ("fprint(\"a...z\") string= "); pfp (a2z = fprint_string (fp, "abcdefghijklmnopqrstuvwxyz")); printf ("\n");
		printf ("fprint(\"a...z\") bits  = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), "abcdefghijklmnopqrstuvwxyz", 26)); printf ("\n");
		printf ("fprint(\"a...z\") concat= "); pfp (fprint_concat (fp, a2l, m2z, 14)); printf ("\n");
		printf ("\n");
		printf ("fprint(\"a.za.z\")normal= "); pfp (a2za2z = fprint_extend (fp, fprint_empty (fp), "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", 52)); printf ("\n");
		printf ("fprint(\"a.za.z\") bytes= "); pfp (fprint_extend_bybyte (fp, fprint_empty (fp), "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", 52)); printf ("\n");
		printf ("fprint(\"a.za.z\") bits = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", 52)); printf ("\n");
		printf ("fprint(\"a.za.z\")concat= "); pfp (fprint_concat (fp, a2z, a2z, 26)); printf ("\n");
		printf ("fprint(\"a.za.z\")extend= "); pfp (fprint_extend (fp, a2z, "abcdefghijklmnopqrstuvwxyz", 26)); printf ("\n");
		printf ("fprint(\"a.za.z\")cncat4= "); pfp (fprint_concat (fp, a2l, fprint_concat (fp, m2z, a2z, 26), 40)); printf ("\n");
		printf ("\n");
		printf ("fprint(\"rand\") bits   = "); pfp (fprint_extend_bybit (fp, fprint_empty (fp), buf, BSIZ)); printf ("\n");
		printf ("fprint(\"rand\") bytes  = "); pfp (fprint_extend_bybyte (fp, fprint_empty (fp), buf, BSIZ)); printf ("\n");
		printf ("fprint(\"rand\") normal = "); pfp (fprint_extend (fp, fprint_empty (fp), buf, BSIZ)); printf ("\n");
		f = fprint_empty (fp);
		for (i = 0; i != NUMKB; i++) {
			f = fprint_extend (fp, f, &buf[i * 1024], 1024);
		}
		printf ("fprint(\"rand\") 1k     = "); pfp (f); printf ("\n");
		f = fprint_empty (fp);
		for (i = 0; i != BSIZ; i++) {
			f = fprint_concat (fp, fprint_extend (fp, fprint_empty (fp), &buf[BSIZ-i-1], 1), f, i);
		}
		printf ("fprint(\"rand\")revconca= "); pfp (f); printf ("\n");
		printf ("\n");
		printf ("slide word:\n");
		s = fprint_extend (fp, fprint_empty (fp), "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0", 24);
		pfp (s); printf ("\n");
		s = fprint_slideword (fp, s, 0, 0);
		pfp (s); printf ("\n");
		s = fprint_concat (fp, 0, 0, 24);
		pfp (s); printf ("\n");
		printf ("\n");
		s = fprint_extend (fp, fprint_empty (fp), "\1\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0", 24);
		pfp (s); printf ("\n");
		s = fprint_slideword (fp, s, 1, 1);
		pfp (s); printf ("\n");
		printf ("\n");
		s = fprint_extend (fp, fprint_empty (fp), "\1\0\0\0\0\0\0\0\2\0\0\0\0\0\0\0\3\0\0\0\0\0\0\0", 24);
		s = fprint_slideword (fp, s, 1, 4);
		pfp (s); printf ("\n");
		s = fprint_extend (fp, fprint_empty (fp), "\2\0\0\0\0\0\0\0\3\0\0\0\0\0\0\0\4\0\0\0\0\0\0\0", 24);
		pfp (s); printf ("\n");
		printf ("\n");
		l = (sizeof (w) / sizeof (w[0])) - 3;
		k = (sizeof (w) / sizeof (w[0])) - 2;
		j = (sizeof (w) / sizeof (w[0])) - 1;
		/* s = fprint_extend (fp, fprint_empty (fp), &w[l], sizeof (w[0]) * 3); */
		/*
		s = fprint_concat (fp, 0, 0, 24);
		s = fprint_slideword (fp, s, 0, w[l]);
		s = fprint_slideword (fp, s, 0, w[k]);
		s = fprint_slideword (fp, s, 0, w[j]);
		*/
		s = fprint_extend_word (fp, fprint_empty (fp), &w[l], 3);
		for (i = 0; i != sizeof (w) / sizeof (w[0]); i++) {
			s = fprint_slideword (fp, s, w[l], w[i]);
			pfp (s);
			printf (" ");
			l = k;
			k = j;
			j = i;
		}
		printf ("\n");
		k = (sizeof (w) / sizeof (w[0])) - 2;
		j = (sizeof (w) / sizeof (w[0])) - 1;
		for (i = 0; i != sizeof (w) / sizeof (w[0]); i++) {
			fprint_uint64_t bb[3];
			bb[0] = w[k];
			bb[1] = w[j];
			bb[2] = w[i];
			pfp (fprint_extend (fp, fprint_empty (fp), bb, sizeof (bb)));
			printf (" ");
			k = j;
			j = i;
		}
		printf ("\n");
		k = (sizeof (w) / sizeof (w[0])) - 2;
		j = (sizeof (w) / sizeof (w[0])) - 1;
		for (i = 0; i != sizeof (w) / sizeof (w[0]); i++) {
			fprint_uint64_t bb[3];
			bb[0] = w[k];
			bb[1] = w[j];
			bb[2] = w[i];
			pfp (fprint_extend_word (fp, fprint_empty (fp), bb, sizeof (bb) / sizeof(w[0])));
			printf (" ");
			k = j;
			j = i;
		}
		printf ("\n");
		printf ("\n");
		fprint_close (fp);
	}
	free (buf);
#if defined(MIKES_WORLD)
	mi_malloc_report ();
#endif
	return (0);
}
#endif
