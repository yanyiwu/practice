all:
	g++ -c myclass.cpp -o myclass.o
	g++ -c interface.cpp -o interface.o
	ar rs libinterface.a interface.o myclass.o
	gcc -c main.c -o main.o
	gcc -o main main.o -L. -linterface -lstdc++
	#gcc -o main main.o -L. -linterface -lstdc++
