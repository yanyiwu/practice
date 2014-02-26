#if !defined(_ENDIAN_H_)
#define _ENDIAN_H_

#if defined(pdp11) || defined(vax) || defined(__alpha) || defined(i386) || defined(__i386) || defined(__i386__) || defined(_M_IX86) || defined(MIPSEL) || defined(_MSC_VER)
#define ENDIAN_LITTLE 1
#endif
#if defined(__sparc__) || defined(MIPSEB)
#define ENDIAN_LITTLE 0
#endif


#if !defined(ENDIAN_LITTLE)
static short _endian_little = 1;
#define ENDIAN_LITTLE (*(char *)&_endian_little)
#endif

#define ENDIAN_BIG (!ENDIAN_LITTLE)

#endif
