package main

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
)

var dbhost string = "127.0.0.1:3306"
var dbuser string = "inforyoumation"
var dbpassword string = ""
var db string = "inforyoumation"

type Book struct {
	Name   string
	Num    int64 `orm:"pk;auto"`
	Author string
	Price  float32
}

func init() {
	orm.RegisterModel(new(Book))
	orm.RegisterDriver("mysql", orm.DR_MySQL)
	conn := dbuser + ":" + dbpassword + "@/" + db + "?charset=utf8"
	orm.RegisterDataBase("default", "mysql", conn)
}

func createTable() {
	name := "default"
	force := false
	verbose := true
	if err := orm.RunSyncdb(name, force, verbose); err != nil {
		beego.Error(err)
	}
}

func main() {
	o := orm.NewOrm()
	o.Using("default")
	createTable()

	var book1 *Book = &Book{Name: "Bob", Price: 30.0, Author: "yanyiwu"}
	var book2 *Book = new(Book)
	book2.Author = "mq"
	book2.Name = "mq111fas"
	book2.Price = 100.0

	fmt.Println(o.Insert(book1))
	fmt.Println(o.Insert(book2))

	books := []Book{
		{Name: "name1", Price: 10},
		{Name: "name2", Price: 12},
		{Name: "name3", Price: 13},
		{Name: "name4", Price: 14},
		{Name: "name5", Price: 15},
	}

	o.InsertMulti(len(books), books)
	fmt.Println(books)

	book := new(Book)
	book.Num = 1
	o.Read(book)
	fmt.Println(book)
	book.Author = "qqq"
	o.ReadOrCreate(book, "Author")
	fmt.Println(book)

	book4 := new(Book)
	book4.Num = 8
	book4.Author = "yanyiwu"
	o.Update(book4, "Author")
	fmt.Println(book4)

	book3 := new(Book)
	book3.Num = 6
	o.Read(book3)
	fmt.Println(book3)
	o.Delete(book3)
}
