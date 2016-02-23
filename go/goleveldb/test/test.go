package main

import (
	"fmt"

	"github.com/syndtr/goleveldb/leveldb"
	"github.com/syndtr/goleveldb/leveldb/util"
)

func main() {
	db, err := leveldb.OpenFile("/tmp/goleveldbtest", nil)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	//err = db.Put([]byte("hello"), []byte("world"), nil)
	//if err != nil {
	//	panic(err)
	//}
	data, err := db.Get([]byte("hello"), nil)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(data))

	iter := db.NewIterator(nil, nil)
	for iter.Next() {
		key := iter.Key()
		value := iter.Value()
		fmt.Println(string(key), string(value))
	}
	iter.Release()

	err = iter.Error()
	if err != nil {
		panic(err)
	}

	iter = db.NewIterator(util.BytesPrefix([]byte("hel")), nil)
	for iter.Next() {
		key := iter.Key()
		value := iter.Value()
		fmt.Println(string(key), string(value))
	}
	iter.Release()

	err = iter.Error()
	if err != nil {
		panic(err)
	}
}
