package main

import (
    "encoding/json"
    "fmt"
    "time"
    "./t2"
)

type A struct {
    Content string
}

func (this A) String() string {
    return "12344"
}

func f1() {
    res, _ := json.Marshal([]string{"apple", "peach", "pear"})
    fmt.Printf(string(res))
    var a A;
    fmt.Printf("%s", a)
    ch := make(chan int, 1)
    ch <- 1
    select {
    case ch <- 2:
        fmt.Printf("ch 222")
    //default:
    //    fmt.Printf("channel is full")
    }
    
    //<- ch

    //go 
    //select {
    //    case 
    //}
}

func f2() {
    ch := make(chan int, 1)
    for {
        select {
        case ch <- 0:
        case ch <- 1:
        default:
            fmt.Println(2)
        }
        i :=  <-ch
        fmt.Println(i)
    }
}

//timeout example
func f3() {
    timeout := make (chan bool, 1)
    go func() {
        time.Sleep(1e9) // sleep one second
        timeout <- true
    }()
    ch := make (chan int)
    select {
    case <- ch:
    case <- timeout:
        fmt.Println("timeout!")
    }
}

// channel is full
func f4() {
    ch := make (chan int, 1)
    ch <- 1
    select {
    case ch <- 2:
    default:
        fmt.Println("channel is full !")
    }
    i := <-ch
    fmt.Println(i)
    //i = <-ch
    //fmt.Println(i)
}

// channel is blocking
func f5() {
    ch := make (chan int, 1)
    ch <- 1
    select {
    case ch <- 2:
    //default:
    //    fmt.Println("channel is full !")
    }
    //i := <-ch
    //fmt.Println(i)
    //i = <-ch
    //fmt.Println(i)
}

func main() {
    //f5()
    var a t2.A2;
    fmt.Println(a.A3)
}
