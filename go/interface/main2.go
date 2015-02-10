package main

import (
//"fmt"
)

func f1(data ...interface{}) {
	println(len(data))
	for i := 0; i < len(data); i++ {
		switch data[i].(type) {
		case int:
			println(data[i].(int))
		case string:
			println(data[i].(string))
		}
	}
}

func main() {
	f1()
	f1(1)
	f1("123")
}
