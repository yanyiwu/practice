package main

import "sort"

type point struct {
	x int
	y int
}

type points []point

func (ps points) Len() int {
	return len(ps)
}

func (ps points) Less(i, j int) bool {
	return ps[i].x < ps[j].x
}

func (ps points) Swap(i, j int) {
	ps[i], ps[j] = ps[j], ps[i]
}

func main() {
	s := points{{2, 1}, {1, 4}, {3, 1}}
	sort.Sort(s)
	for i := 0; i < len(s); i++ {
		println(s[i].x, s[i].y)
	}
}
