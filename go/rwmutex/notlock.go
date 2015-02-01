package main

import (
	//"sync"
	"math/rand"
	"runtime"
	"strconv"
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
			g = Tmp{rand.Intn(100), strconv.Itoa(rand.Intn(100)), rand.Float64()}
			println("set", g.a)
		}
	}()
	go func() {
		for {
			println("get", g.a)
			println("get", g.c)
			println("get", g.b)
		}
	}()
	go func() {
		for {
			println("get", g.a)
			println("get", g.c)
			println("get", g.b)
		}
	}()
	go func() {
		for {
			println("get", g.a)
			println("get", g.c)
			println("get", g.b)
		}
	}()
	for {
		time.Sleep(30 * time.Second)
	}
}
