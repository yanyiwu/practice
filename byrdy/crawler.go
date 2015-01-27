package main

import (
	"github.com/aszxqw/igo"
)

func main() {
	print(string(igo.HttpGet("http://bbs.byr.cn/rss/board-Advertising")))
}
