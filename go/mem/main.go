package main

import "sync"
import "fmt"

var a string
var once sync.Once

func setup() {
	a = "hello, world"
	print(a)
}

func doprint() {
	print("doprint\n")
	once.Do(setup)
	print("\n")
}

func twoprint() {
	go doprint()
	go doprint()
}

func main() {
	twoprint()
	var a int
	fmt.Scanln(&a)
}
