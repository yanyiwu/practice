package main

import (
	"fmt"
	"time"
)

var x int

func main() {
	go func() {
		for {
			x = 1
		}
	}()
	go func() {
		for {
			fmt.Println(x)
		}
	}()
	time.Sleep(50 * time.Second)
}
