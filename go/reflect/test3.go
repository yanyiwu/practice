package main

import (
	"fmt"
	"reflect"
)

func main() {
	type T struct {
		Header int    `redis:"header"`
		Body   string `redis:"body"`
	}
	t := T{23, "skidoo"}
	s := reflect.ValueOf(&t).Elem()
	typeOfT := s.Type()
	for i := 0; i < s.NumField(); i++ {
		f := s.Field(i)
		fmt.Printf("%d: %s %s %s = %v\n", i,
			typeOfT.Field(i).Name, f.Type(), reflect.TypeOf(t).Field(i).Tag.Get("redis"), f.Interface())
	}
}
