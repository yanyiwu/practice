package main

import (
	"net/http"
)

func HelloServer1(w http.ResponseWriter, r *http.Request) {
	//r.ParseForm()
	val := r.FormValue("key")
	println("HelloServer1", val)
	w.Write([]byte(val))
}

func HelloServer2(w http.ResponseWriter, r *http.Request) {
	//r.ParseForm()
	_, fe := r.MultipartReader()
	if fe != nil {
		println("HelloServer2", fe)
		return
	}
	val := r.FormValue("key")
	println("HelloServer2", val)
	w.Write([]byte(val))
}
func HelloServer3(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	_, fe := r.MultipartReader()
	if fe != nil {
		println("HelloServer3", fe)
		return
	}
	val := r.FormValue("key")
	println("HelloServer3", val)
	w.Write([]byte(val))
}

func main() {
	http.HandleFunc("/hello1", HelloServer1)
	http.HandleFunc("/hello2", HelloServer2)
	http.HandleFunc("/hello3", HelloServer3)
	println("start ...")
	err := http.ListenAndServe(":8888", nil)
	if err != nil {
		println("error", err)
	}
}
