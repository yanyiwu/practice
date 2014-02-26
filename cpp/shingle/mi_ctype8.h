
#if !defined(_MI_CTYPE8_H_)
#define _MI_CTYPE8_H_

extern const unsigned char *_mi_ctype8__;
extern const unsigned char *_mi_tolower8__;
extern const unsigned char *_mi_toupper8__;
extern const unsigned char *_mi_toascii8__;

#define mi_isalnum8(_c)	(_mi_ctype8__[_c]&(_MI_U|_MI_L|_MI_D))
#define mi_isalpha8(_c)	(_mi_ctype8__[_c]&(_MI_U|_MI_L))
#define mi_iscntrl8(_c)	(_mi_ctype8__[_c]&(_MI_C|_MI_B))
#define mi_isdigit8(_c)	(_mi_ctype8__[_c]&(_MI_D))
#define mi_isgraph8(_c)	(_mi_ctype8__[_c]&(_MI_U|_MI_L|_MI_D|_MI_P))
#define mi_islower8(_c)	(_mi_ctype8__[_c]&(_MI_L))
#define mi_isprint8(_c)	(_mi_ctype8__[_c]&(_MI_U|_MI_L|_MI_D|_MI_P|_MI_S))
#define mi_ispunct8(_c)	(_mi_ctype8__[_c]&(_MI_P))
#define mi_isspace8(_c)	(_mi_ctype8__[_c]&(_MI_B|_MI_S))
#define mi_isupper8(_c)	(_mi_ctype8__[_c]&(_MI_U))
#define mi_isxdigit8(_c)	(_mi_ctype8__[_c]&(_MI_X|_MI_D))
#define mi_tolower8(_c)	(_mi_tolower8__[_c])
#define mi_toupper8(_c)	(_mi_toupper8__[_c])

#define mi_isascii8(_c)	((_c) & 0x80)
#define mi_toascii8(_c)	(_mi_toascii8__[_c])

#define	_MI_U	0x01
#define	_MI_L	0x02
#define	_MI_D	0x04
#define	_MI_S	0x08
#define	_MI_B	0x10
#define _MI_P	0x20
#define _MI_C	0x40
#define _MI_X	0x80

enum mi_ctype8_set {
	mi_ctype8_iso_latin_1
};

void mi_ctype8_charset (enum mi_ctype8_set set);

#endif
