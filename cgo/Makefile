all: libfoo.so
	go build
libfoo.so:
	gcc -shared -o libfoo.so foo.c
clean:
	rm -f *.o *.so cgo
