package main

import "fmt"

func main() {
	x := make(map[string]int)
	fmt.Println(x)
	x["hello"] = 1
	fmt.Println(x)
	if x["hello2"] == 1 {
		fmt.Println("yes")
	} else {
		fmt.Println("no")
	}
	y := x["hello3"]
	fmt.Println(x)
	fmt.Println(y)
	x["hello3"] = y
	fmt.Println(x)
}
