package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"time"

	"github.com/yanyiwu/gojieba"
)

func main() {
	jieba := gojieba.NewJieba("./jieba.dict.utf8", "./hmm_model.utf8", "user.dict.utf8")
	defer jieba.Free()
	lines := []string{}
	f, err := os.Open("../../../nodejs/nodejieba/performance/weicheng.utf8")
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
			jieba.Cut(lines[j], true)
		}
	}
	fmt.Println(time.Now())
}
