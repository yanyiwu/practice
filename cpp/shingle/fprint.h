
#if !defined(_FPRINT_H_)
#define _FPRINT_H_

#include <string.h>
#include "fprint.h"
#include "endian.h"

#if defined(__GNUC__)
typedef long long fprint_int64_t;
typedef unsigned long long fprint_uint64_t;
#endif

#if defined(_MSC_VER)
typedef __int64 fprint_int64_t;
typedef unsigned __int64 fprint_uint64_t;
#endif

typedef fprint_uint64_t fprint_t;
/* the type of a 64-bit fingerprint */

typedef struct fprint_data_s *fprint_data_t;
/* an opaque type used to keep the data structures need to compute
   fingerprints.  */

fprint_data_t fprint_new (fprint_t poly, unsigned span);
/* Computes the tables needed for fingerprint manipulations.
   Requires that "poly" be the binary representation
   of an irreducible polynomial in GF(2) of degree 64.   The X^64 term
   is not represented.  The X^0 term is the high order bit, and the
   X^63 term is the low-order bit.
   
   span is used in later calls to fprint_slide_word().
   If fprint_slide_word() is not to be called, span should be set to zero. */

fprint_t fprint_empty (fprint_data_t fp);
/* returns the fingerprint of the empty string */

fprint_t fprint_extend (fprint_data_t fp, fprint_t a, void *data, unsigned len);
/* if fp was generated with polynomial P,
   "a" is the fingerprint under P of string A, and bytes "data[0, ..., len-1]"
   contain string B, return the fingerprint under P of the concatenation of A and B.
   Strings are treated as polynomials.  The low-order bit in the first byte is the
   highest degree coefficient in the polynomial. 
   This routine differs from fprint_extend_word() in that it will read bytes in
   increasing address order, regardless of the endianness of the machine.  */

fprint_t fprint_extend_word (fprint_data_t fp, fprint_t a, fprint_uint64_t *data, unsigned len);
/* If fp was generated with polynomial P,
   "a" is the fingerprint under P of string A, and 64-bit words "data[0, ..., len-1]"
   contain string B, return the fingerprint under P of the concatenation of A and B.
   Arrays of words are treated as polynomials.  The low-order bit in the first word is the
   highest degree coefficient in the polynomial. 
   This routine differs from fprint_extend() on bigendian machines,
   where the byte order within each word is backwards. */

fprint_t fprint_concat (fprint_data_t fp, fprint_t a, fprint_t b, fprint_t blen);
/* if fp was generated with polynomial P,
   "a" is the fingerprint under P of string A, and "b" is the fingerprint under P
   of string B, which has length "blen" bytes,
   return the fingerprint under P of the concatenation of A and B */

void fprint_output (void (*outc) (int c, void *v), void *v, fprint_t f);
/* Turn fingerprint "f" into a hexadecimal,
   ascii-zero-filled printable string S of length 16,
   and call "(*outc) (c, v)" on each character "c" in S. */

void fprint_toascii (fprint_t f, char *buf);
/* Turn fingerprint "f" into a hexadecimal, 
   ascii-zero-filled printable string S of length 16,
   and place the characters in buf[0,...,15].
   No null terminator is written by the routine. */

fprint_t fprint_slideword (fprint_data_t fp, fprint_t f, fprint_uint64_t a, fprint_uint64_t b);
/* if "fp" was generated with polynomial P,
   X is some string of length "(span-1)*sizeof (fprint_uint64_t)" bytes  (see fprint_new()),
   "f" is the fingerprint under P of word "a" concatenated with X, 
   return the fingerprint under P of X concatenated with word "b".
   The words "a" and "b" represent polynomials whose X^0 term is in the high-order bit,
   and whose X^63 term is in the low order bit.  */

void fprint_close (fprint_data_t fp);
/* discard the data associated with "fp" */

extern const fprint_t fprint_polys[];
extern const int fprint_npolys;
/* fprint_polys[0,...,fprint_npolys-1] are unique, degree-64 polynomials
   suitable for use as "poly" arguments to fprint_new().
   fprint_npolys >= 10.  */

#endif
