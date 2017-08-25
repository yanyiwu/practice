package main

import (
	"fmt"
	"strings"

	"github.com/yanyiwu/gojieba"
)

func main() {
	var s string
	var words []string
	x := gojieba.NewJieba()
	defer x.Free()
	s = "山东苹果"
	words = x.Cut(s, false)
	fmt.Println("cut:", strings.Join(words, "/"))
	x.AddWord("山东")
	words = x.Cut(s, false)
	fmt.Println("cut:", strings.Join(words, "/"))
}
