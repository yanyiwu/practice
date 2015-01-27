package main

import (
	"encoding/xml"
	//"fmt"
	"io/ioutil"
	"log"
	//"reflect"
)

type Rss struct {
	//Version string    `xml:"version,attr"`
	Channel Channel `xml:"channel"`
}
type Channel struct {
	Title         string `xml:"title"`
	Description   string `xml:"description"`
	Link          string `xml:"link"`
	Language      string `xml:"language"`
	Generator     string `xml:"generator"`
	LastBuildDate string `xml:"lastBuildDate"`
	Items         []Item `xml:"item"`
}
type Item struct {
	Title       string `xml:"title"`
	Link        string `xml:"link"`
	Author      string `xml:"author"`
	PubDate     string `xml:"pubDate"`
	Guid        string `xml:"guid"`
	Comments    string `xml:"comments"`
	Description string `xml:"description"`
}

func main() {
	content, err := ioutil.ReadFile("1.xml")
	if err != nil {
		log.Fatal(err)
	}

	content = []byte(convert(string(content)))

	var rss Rss
	err = xml.Unmarshal(content, &rss)
	if err != nil {
		log.Fatal(err)
	}
	//fmt.Println(rss)
	for i := 0; i < len(rss.Channel.Items); i++ {
		println(rss.Channel.Items[i].Title)
	}
}
