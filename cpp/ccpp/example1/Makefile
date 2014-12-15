all:
	g++ -c c_api.cpp -o c_api.o
	ar rs libfoo.a c_api.o
	gcc -c cfoo.c -o cfoo.o
	gcc -o cfoo cfoo.o -L. -lfoo -lstdc++
foo_test:
	g++ -o foo_test foo_test.cpp
