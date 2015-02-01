package main

import (
	//"sync"
	"math/rand"
	"runtime"
	"time"
)

type Tmp struct {
	a int
	b string
	c float64
}

var g Tmp

func main() {
	runtime.GOMAXPROCS(4)
	go func() {
		for {
			g = Tmp{rand.Intn(100), "123", rand.Float64()}
			println("set", g.a)
		}
	}()
	go func() {
		for {
			println("get", g.c)
		}
	}()
	for {
		time.Sleep(30 * time.Second)
	}
}
