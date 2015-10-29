package main

import "fmt"

func main() {
	// x是数组，数组的元素是指针，指针的指向是数组，数组的元素是指针，指针指向的是int
	// y是数组，数组的元素是指针，指针的指向是int
	var x [5]*[5]*int
	var y [5]*int
	x[0] = &y
	fmt.Printf("%v\n", y)
	fmt.Printf("%v\n", x)
}
