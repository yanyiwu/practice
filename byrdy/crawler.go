package main

import (
	"github.com/yanyiwu/igo"
)

func main() {
	print(string(igo.HttpGet("http://bbs.byr.cn/rss/board-Advertising")))
}
