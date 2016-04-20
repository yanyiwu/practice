package main

import (
	"sync"
	"sync/atomic"
)

type Once struct {
	m    sync.Mutex
	done uint32
}

func (once *Once) Do(f func()) {
	if atomic.LoadUint32(&once.done) == 1 {
		return
	}
	once.m.Lock()
	defer once.m.Unlock()
	if once.done == 0 {
		defer atomic.StoreUint32(&once.done, 1)
		f()
	}
}
