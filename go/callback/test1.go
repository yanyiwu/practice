package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func RequestCallBack(url string, cb func(string)) {
	var body []byte
	var err error
	go func() {
		var resp *http.Response
		resp, err = http.Get(url)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer resp.Body.Close()
		body, _ = ioutil.ReadAll(resp.Body)
		cb(string(body))
	}()
}

func main() {
	cb := func(s string) {
		fmt.Println(s)
	}
	RequestCallBack("http://yanyiwu.com", cb)
	var tmp string
	fmt.Scanln(&tmp)
}
