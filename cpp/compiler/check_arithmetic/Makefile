cc=gcc
calc:calc.y calc.l
	bison -d calc.y
	flex -o calc.lex.c calc.l
	cc -o $@ calc.tab.c calc.lex.c -lfl 

calc.lex: calc.y calc.l
	bison -d calc.y 
	flex -o calc.lex.c calc.l 
	cc -D CALC_LEX -o $@ calc.lex.c -lfl 
clean:
	rm -f calc.lex.c
	rm -f calc.tab.h
	rm -f calc.tab.c
	rm -f calc
test:
	echo "|2-4|*3-2/(1+3) " | ./calc
run:
	./calc
