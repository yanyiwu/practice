package main

import (
	"fmt"
	"log"
	"net/http"
)

func procRequest(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	w.Header().Set("Content-Type", "text/json")
	fmt.Fprintf(w, string(`{"key": "hello golang"}`))
}

func main() {
	http.HandleFunc("/", procRequest)
	err := http.ListenAndServe(":8888", nil)
	if err != nil {
		log.Fatal("ListenAndServe failed, ", err)
	}
}
