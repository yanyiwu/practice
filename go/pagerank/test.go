package main

import (
	"fmt"
	"strconv"
	"strings"
)

const X = `
0    0.5 1 0
0.33 0   0 0.5
0.33 0   0 0.5
0.33 0.5 0 0
`

func Filter(strs []string, f func(string) bool) []string {
	res := make([]string, 0, len(strs))
	for _, s := range strs {
		if f(s) {
			res = append(res, s)
		}
	}
	return res
}

func MapToFloat64(strs []string) []float64 {
	res := make([]float64, 0, len(strs))
	for _, s := range strs {
		v, err := strconv.ParseFloat(s, 64)
		if err != nil {
			panic(err)
		}
		res = append(res, v)
	}
	return res
}

func Parse(s string) [][]float64 {
	x := Filter(strings.Split(strings.Trim(s, "\n "), "\n"), func(s string) bool {
		return strings.TrimSpace(s) != ""
	})
	n := len(x)
	result := make([][]float64, 0, n)
	for i := 0; i < len(x); i++ {
		y := Filter(strings.Split(strings.Trim(x[i], " "), " "), func(s string) bool {
			return strings.TrimSpace(s) != ""
		})
		if len(y) != n {
			panic("data illegal")
		}
		fmt.Println(strings.Join(y, "/"))
		result = append(result, MapToFloat64(y))
	}
	return result
}

func main() {
	fmt.Println(Parse(X))
}
