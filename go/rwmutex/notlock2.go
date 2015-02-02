package main

import (
	//"sync"
	"math/rand"
	"runtime"
	//"strconv"
	"time"
)

type Tmp struct {
	a int
	b string
	c float64
}

var g map[int]int = make(map[int]int)

func main() {
	runtime.GOMAXPROCS(4)
	g[1] = 1
	go func() {
		for {
			g[rand.Intn(100000)] = rand.Intn(10000)
		}
	}()
	go func() {
		for {
			for k, v := range g {
				println(k, v)
			}
		}
	}()
	for {
		time.Sleep(30 * time.Second)
	}
}
