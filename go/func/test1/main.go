package main

func Foo(s string, f func(s string) string) string {
	return f(s) + "123"
}

func main() {
	f := func(s string) string {
		return s + "321"
	}
	s := Foo("x", f)
	println(s)
	println(f != nil)
	f = nil
	println(f != nil)
}
