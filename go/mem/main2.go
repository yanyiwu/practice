package main

import "sync"
import "fmt"
import "time"

var once sync.Once

var a string
var done bool

func setup() {
	done = true
	time.Sleep(1000 * time.Millisecond)
	a = "hello, world\n"
}

func doprint() {
	if !done {
		once.Do(setup)
	}
	print(a)
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
