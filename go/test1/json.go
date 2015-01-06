package main

import (
	"encoding/json"
	"fmt"
)

type Message struct {
	Name string
	Body string
	Time int64
}

func main() {
	m := Message{"Alice&Jim", "Hello", 1294706395881547000}
	b, err := json.Marshal(m)
	if err != nil {
		return
	}

	fmt.Println(string(b))
}
