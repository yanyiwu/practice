package main

import "fmt"

func t1() {
	x := [3]int{1, 2, 3}
	var sx []int = x[:]
	sx[0] = 111
	fmt.Println(x)
	fmt.Println(sx)
}

func t2() {
	x := [3]int{1, 2, 3}
	var sx []int
	sx = make([]int, 3)
	copy(sx, x[0:])
	sx[0] = 111
	fmt.Println(x)
	fmt.Println(sx)
}

func t3() {
	sx := []int{1, 2, 3}
	sy := sx
	sy[0] = 111
	fmt.Println(sx)
	fmt.Println(sy)
}
func t4() {
	sx := []int{1, 2, 3}
	sy := []int{0, 0, 0}
	copy(sy, sx)
	sy[0] = 111
	fmt.Println(sx)
	fmt.Println(sy)
}

func main() {
	fmt.Println("t1")
	t1()
	fmt.Println("t2")
	t2()
	fmt.Println("t3")
	t3()
	fmt.Println("t4")
	t4()
}
