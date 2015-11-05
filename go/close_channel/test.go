package main

import "fmt"

func main() {
	jobs := make(chan int, 5)
	done := make(chan bool, 1)

	go func() {
		for {
			x, more := <-jobs
			if more {
				fmt.Printf("receive x: %d\n", x)
			} else {
				fmt.Printf("receive all jobs.")
				done <- true
				return
			}
		}
	}()

	for i := 0; i < 3; i++ {
		jobs <- i
	}
	close(jobs)
	<-done
}
