package main

import (
	"fmt"
	"time"
)

func main() {
	t, _ := time.Parse(time.RFC1123, "Fri, 27 Feb 2015 05:39:23 GMT")
	fmt.Println(t.Day())
	fmt.Println(time.Now())
}
