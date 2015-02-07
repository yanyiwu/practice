package main

type A interface {
	GetTitle() string
}

type B struct {
	t string
}

func (b *B) GetTitle() string {
	return b.t
}

func main() {
	var b B
	b.t = "1234"
	println(b.GetTitle())
	a := &b
	println(a.GetTitle())

	c := make([]A, 0)
	c = append(c, &b)
	println(c[0].GetTitle())
}
