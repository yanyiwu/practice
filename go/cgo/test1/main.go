package main

/*
#include "hello.h"
*/
import "C"

func Run() {
	C.SayHi()
}

func main() {
	Run()
}
