package main

import "fmt"

func main() {
    fmt.Println("Hello, world.")
    ch := make(chan int, 1)
    for {
        select {
        case ch <- 0:
        case ch <- 1:
        }
        i := <-ch
        fmt.Println("Value received: ", i)
    }
}
