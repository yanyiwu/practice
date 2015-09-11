// foo.go
package foo

/*
#include "foo.h"
*/
import "C"

//import "unsafe"

type GoFoo struct {
	foo C.Foo
}

func New() GoFoo {
	var ret GoFoo
	ret.foo = C.FooInit()
	return ret
}
func (f GoFoo) Free() {
	//C.FooFree(unsafe.Pointer(f.foo))
	C.FooFree(f.foo)
}
func (f GoFoo) Bar() {
	//C.FooBar(unsafe.Pointer(f.foo))
	C.FooBar(f.foo)
}
