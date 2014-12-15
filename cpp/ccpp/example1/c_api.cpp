#include "foo.hpp"

using foons::Foo;

extern "C" {
    Foo * NewFoo()
    {
        Foo * foo = new Foo();
        return foo;
    }
    void FreeFoo(Foo * foo)
    {
        delete foo;
    }
    void FooHello(Foo * foo)
    {
        foo->Hello();
    }
}
