package main

import (
	"mime"
)

func main() {
	m := mime.TypeByExtension(".json")
	println(m)
	m = mime.TypeByExtension(".mp3")
	println(m)
}
