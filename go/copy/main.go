package main

import "fmt"

type Foo struct {
	s   string
	i   int
	arr []int
}

func main() {
	foo := &Foo{}
	foo.s = "hehe"
	foo.i = 1
	foo.arr = make([]int, 0)
	foo.arr = append(foo.arr, 1)
	bar := Foo{}
	bar = *foo
	bar.arr = make([]int, 0)
	bar.arr = append(bar.arr, 2)
	fmt.Println(foo)
	fmt.Println(bar)
}
