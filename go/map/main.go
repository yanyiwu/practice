package main

func main() {
	mp := make(map[string]struct{}, 0)
	for key, _ := range mp {
		println(key)
	}
	mp["1"] = struct{}{}
	for key, _ := range mp {
		println(key)
	}
}
