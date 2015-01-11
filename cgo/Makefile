all: libfoo.so
	go build
libfoo.so: foo.c
	gcc -fPIC -shared -o libfoo.so foo.c
clean:
	rm -f *.o *.so cgo
