package main

import (
	//"sync"
	"math/rand"
	"runtime"
	//"strconv"
	"time"
)

//type Tmp struct {
//	a int
//	b string
//	c float64
//}

var g int

func main() {
	runtime.GOMAXPROCS(4)
	go func() {
		for {
			g = rand.Intn(10000000)
			println("set", g)
		}
	}()
	go func() {
		for {
			println("get", g)
		}
	}()
	go func() {
		for {
			println("get", g)
		}
	}()
	go func() {
		for {
			println("get", g)
		}
	}()
	for {
		time.Sleep(30 * time.Second)
	}
}
