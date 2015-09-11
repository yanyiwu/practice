boolean:boolean.y boolean.l
	bison -d boolean.y
	flex -o boolean.lex.c boolean.l
	cc -o $@ boolean.tab.c boolean.lex.c -lfl 

boolean.lex: boolean.y boolean.l
	bison -d boolean.y 
	flex -o boolean.lex.c boolean.l 
	cc -D CALC_LEX -o $@ boolean.lex.c -lfl 
clean:
	rm boolean.lex.c
	rm boolean.tab.h
	rm boolean.tab.c
	rm boolean
test:
	echo "true and true" | ./boolean
	echo "true and false" | ./boolean
	echo "true and false" | ./boolean
	echo "true and (true and false)" | ./boolean
	echo "true and (true and true)" | ./boolean
