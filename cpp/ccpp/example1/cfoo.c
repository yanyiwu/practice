#include <stdio.h>
#include <stdlib.h>

extern struct Foo * NewFoo();
extern void FreeFoo(struct Foo * foo);
extern void FooHello(struct Foo * foo);

int main()
{
    struct Foo* foohandle = NewFoo();
    FooHello(foohandle);
    FreeFoo(foohandle);
    return 0;
}
