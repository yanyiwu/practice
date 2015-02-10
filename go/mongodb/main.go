package main

import (
	"fmt"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
)

type Mail struct {
	Id    bson.ObjectId "_id"
	Name  string
	Email string
}

func main() {
	sess, err := mgo.Dial("127.0.0.1")
	if err != nil {
		panic(err)
	}
	defer sess.Close()

	c := sess.DB("test1").C("test1")
	m1 := Mail{bson.NewObjectId(), "user1", "user1@dotcoo.com"}
	m2 := Mail{bson.NewObjectId(), "user2", "user2@dotcoo.com"}
	m3 := Mail{bson.NewObjectId(), "user3", "user3@dotcoo.com"}
	m4 := Mail{bson.NewObjectId(), "user4", "user4@dotcoo.com"}
	err = c.Insert(&m1, &m2, &m3, &m4)
	if err != nil {
		panic(err)
	}

	ms := []Mail{}
	err = c.Find(&bson.M{"name": "user1"}).All(&ms)

	if err != nil {
		panic(err)
	}

	for i, m := range ms {
		fmt.Printf("%s, %d, %s\n", m.Id.Hex(), i, m.Email)
	}
}
