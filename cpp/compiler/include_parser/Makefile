LEX=flex
YACC=bison
CC=g++
a.out: lex.yy.o frame.tab.o main.o
	$(CC) -o $@ lex.yy.o frame.tab.o main.o
lex.yy.o: lex.yy.c frame.tab.h main.hpp
	$(CC) -c lex.yy.c 
frame.tab.o: frame.tab.c main.hpp
	$(CC) -c frame.tab.c

main.o: main.hpp main.cpp
	$(CC) -c main.cpp
frame.tab.c frame.tab.h: frame.y
	$(YACC) -d frame.y
lex.yy.c: frame.l
	$(LEX) frame.l

clean:
	rm -f *.o *.c *.h
