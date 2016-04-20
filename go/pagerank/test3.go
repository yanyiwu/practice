package main

import (
	"flag"
	"fmt"
)

// output: [0, 0, 0, 0]
//var M [][]float64 = [][]float64{
//	[]float64{0, 1.0 / 3, 1.0 / 3, 1.0 / 3},
//	[]float64{0.5, 0, 0, 0.5},
//	[]float64{0, 0, 0, 0},
//	[]float64{0, 0.5, 0.5, 0},
//}

// output: [0, 0, 1, 0]
var M [][]float64 = [][]float64{
	[]float64{0, 1.0 / 3, 1.0 / 3, 1.0 / 3},
	[]float64{0.5, 0, 0, 0.5},
	[]float64{0, 0, 1, 0},
	[]float64{0, 0.5, 0.5, 0},
}

var V []float64 = []float64{
	0.25, 0.25, 0.25, 0.25,
}

func Multiply(v []float64, m [][]float64) []float64 {
	result := make([]float64, len(v))
	for i := 0; i < len(v); i++ {
		result[i] = 0.0
		for j := 0; j < len(m); j++ {
			result[i] += v[j] * m[j][i]
		}
	}
	return result
}

var n = flag.Int("n", 1, "iteration counts")

func main() {
	flag.Parse()
	v := V
	for i := 0; i < *n; i++ {
		v = Multiply(v, M)
		fmt.Println(v)
	}
	fmt.Println(v)
}
