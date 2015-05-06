all:
	flex wc.l
	gcc -o wc lex.yy.c -lfl
clean:
	rm -f *.c wc
run:
	cat wc.l | ./wc
