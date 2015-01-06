package main

import "fmt"

func test1() {
	a := make(map[string][]string)
	//a["1"] = make([]string, 0)
	b := a["1"]
	if b == nil {
		print("b == nil\n")
	}
	//a["1"] = append(b, "123")
	a["1"] = append(b, "123")
	fmt.Printf("%v", a)
}

func test2() {
	a := make(map[string]map[string]string)
	b := a["1"]
	if b == nil {
		b = make(map[string]string)
	}
	b["2"] = "3"
	a["1"] = b
	fmt.Printf("%v", a)
}

func test3() {
	var a []string = nil
	a = append(a, "123")
	print(a)
}

func main() {
	//test1()
	test2()
	//test3()
}
