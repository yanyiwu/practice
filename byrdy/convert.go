package main

import (
	"github.com/golang/glog"
	"github.com/qiniu/iconv"
	"strings"
)

var ic iconv.Iconv

func init() {
	var err error
	ic, err = iconv.Open("utf-8", "gbk")
	if err != nil {
		glog.Fatal("iconv.Open failed!")
	}
}

func convert(data string) string {
	data = ic.ConvString(data)
	return strings.Replace(data, `encoding="gb2312"`, `encoding="utf-8"`, 1)
}
