package main

import (
	"fmt"
	"reflect"
)

func main() {
	x := struct {
		Foo string
		Bar int
	}{"foo", 2}

	v := reflect.ValueOf(x)

	values := make([]interface{}, v.NumField())

	for i := 0; i < v.NumField(); i++ {
		values[i] = v.Field(i).Interface()
	}

	fmt.Println(values)

	fmt.Println(values[0].(string))
	fmt.Println(values[1].(int))
}
