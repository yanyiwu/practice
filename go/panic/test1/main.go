package main

import "fmt"

func foo() string {
	s := ""
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("panic")
		}
	}()
	s = "foo finished"
	return s
}

func bar() (s string) {
	defer func() {
		if err := recover(); err != nil {
			s = "bar panic"
		}
	}()
	s = "bar finished"
	panic(1)
	return
}

func main() {
	//fmt.Println(foo())
	fmt.Println(bar())
}
