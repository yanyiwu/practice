package main

import "fmt"

var once Once
var foo *Foo

type Foo struct {
}

func (foo *Foo) SayHi() {
	fmt.Println("say hi")
}

func main() {
	once.Do(func() {
		foo = &Foo{}
	})
	foo.SayHi()
}
