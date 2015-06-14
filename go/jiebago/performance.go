package main

import (
	"bufio"
	"fmt"
	"github.com/wangbin/jiebago"
	"io"
	"os"
	"time"
)

var seg jiebago.Segmenter
var t string

func init() {
	seg.LoadDictionary("dict.txt")
}
func print(ch <-chan string) {
	for word := range ch {
		t = word
	}
}

func main() {
	lines := []string{}
	f, err := os.Open("weicheng.utf8")
	defer f.Close()
	if nil == err {
		buff := bufio.NewReader(f)
		for {
			line, err := buff.ReadString('\n')
			if err != nil || io.EOF == err {
				break
			}
			lines = append(lines, line)
		}
	}
	fmt.Println(len(lines))
	fmt.Println(time.Now())
	for i := 0; i < 50; i++ {
		for j := 0; j < len(lines); j++ {
			print(seg.Cut(lines[j], true))
		}
	}
	fmt.Println(time.Now())
}
