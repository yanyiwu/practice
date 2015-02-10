package main

func main() {
	s := "你好"
	for i := 0; i < len(s); i++ {
		println(s[i])
	}
	for _, c := range s {
		println(c)
	}
}
