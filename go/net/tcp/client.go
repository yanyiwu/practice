package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:3333")
	checkError(err)
	_, err = conn.Write([]byte("HEAD"))
	reader := bufio.NewReader(os.Stdin)
	for {
		line, err := reader.ReadString('\n')
		fmt.Println(err)
		line = strings.TrimRight(line, " \t\r\n")
		if err != nil {
			conn.Close()
			break

		}
	}
}
func checkError(err error) {
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
	}
}
