package main

import (
	"fmt"

	"github.com/blevesearch/bleve"
)

func main() {
	// open a new index
	index, err := bleve.Open("example.bleve")
	if err != nil {
		fmt.Println(err)
		return
	}

	// search for some text
	query := bleve.NewMatchQuery("3")
	search := bleve.NewSearchRequest(query)
	searchResults, err := index.Search(search)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(searchResults)
}
