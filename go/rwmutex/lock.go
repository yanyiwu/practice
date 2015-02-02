package main

import (
	"math/rand"
	"runtime"
	"strconv"
	"sync"
	"time"
)

type Tmp struct {
	a int
	b string
	c float64
}

var g map[string]string
var gLock sync.RWMutex

func main() {
	runtime.GOMAXPROCS(4)
	go func() {
		for {
			gLock.Lock()
			//g = Tmp{rand.Intn(100), strconv.Itoa(rand.Intn(100)), rand.Float64()}
			g[strconv.Itoa(rand.Intn(10000))] = strconv.Itoa(rand.Intn())
			println("set", g.a)
			gLock.Unlock()
		}
	}()
	go func() {
		for {
			gLock.RLock()
			println("get", g.a)
			println("get", g.c)
			println("get", g.b)
			gLock.RUnlock()
		}
	}()
	go func() {
		for {
			gLock.RLock()
			println("get", g.a)
			println("get", g.c)
			println("get", g.b)
			gLock.RUnlock()
		}
	}()
	go func() {
		for {
			gLock.RLock()
			println("get", g.a)
			println("get", g.c)
			println("get", g.b)
			gLock.RUnlock()
		}
	}()
	for {
		time.Sleep(30 * time.Second)
	}
}
