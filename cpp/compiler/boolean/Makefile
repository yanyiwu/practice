boolean:boolean.y boolean.l
	bison -d boolean.y
	flex -o boolean.lex.c boolean.l
	cc -o $@ boolean.tab.c boolean.lex.c -lfl 

boolean.lex: boolean.y boolean.l
	bison -d boolean.y 
	flex -o boolean.lex.c boolean.l 
	cc -D CALC_LEX -o $@ boolean.lex.c -lfl 
clean:
	rm -f boolean.lex.c boolean.tab.h boolean.tab.c boolean
test:
	echo "true and true" | ./boolean
	echo "true and false" | ./boolean
	echo "true and false" | ./boolean
	echo "true and ((true or false) and false )" | ./boolean
	echo "true and (true or (false and false ))" | ./boolean
