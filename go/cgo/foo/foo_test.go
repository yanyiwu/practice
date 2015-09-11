package foo

import "testing"

func TestFoo(t *testing.T) {
	foo := New()
	foo.Bar()
	foo.Free()
}
