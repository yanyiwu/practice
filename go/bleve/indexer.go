package main

import (
	"fmt"

	"github.com/blevesearch/bleve"
)

type doc struct {
	Name string
}

func main() {
	// open a new index
	index, err := bleve.New("example.bleve", bleve.NewIndexMapping())
	if err != nil {
		fmt.Println(err)
		return
	}

	// index some data
	index.Index("3", doc{
		Name: "text 3",
	})
	index.Index("2", doc{
		Name: "text 2 3 4 hello world",
	})
	index.Index("1", doc{
		Name: "text 1",
	})

	// search for some text
	//query := bleve.NewMatchQuery("text")
	//search := bleve.NewSearchRequest(query)
	//searchResults, err := index.Search(search)
	//if err != nil {
	//	fmt.Println(err)
	//	return
	//}
	//fmt.Println(searchResults)
}
