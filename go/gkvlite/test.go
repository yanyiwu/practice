package main

import (
	"fmt"
	"os"

	"github.com/steveyen/gkvlite"
)

func HandleError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	dbfile := "/tmp/test.gkvlite"
	f, err := os.Create(dbfile)
	HandleError(err)
	defer os.Remove(dbfile)
	s, err := gkvlite.NewStore(f)
	HandleError(err)
	c := s.SetCollection("cars", nil)

	// You can also retrieve the collection, where c == cc.
	//cc := s.GetCollection("cars")

	// Insert values.
	c.Set([]byte("tesla"), []byte("$$$"))
	c.Set([]byte("mercedes"), []byte("$$"))
	c.Set([]byte("bmw"), []byte("$"))

	// Retrieve values.
	mercedesPrice, err := c.Get([]byte("tesla"))
	HandleError(err)
	fmt.Println(mercedesPrice)

	// Replace values.
	c.Set([]byte("tesla"), []byte("$$$$"))

	// Retrieve values.
	mercedesPrice, err = c.Get([]byte("tesla"))
	HandleError(err)
	fmt.Println(mercedesPrice)

	// One of the most priceless vehicles is not in the collection.
	thisIsNil, err := c.Get([]byte("the-apollo-15-moon-buggy"))
	HandleError(err)
	fmt.Println(thisIsNil)

	// Iterate through items.
	c.VisitItemsAscend([]byte("ford"), true, func(i *gkvlite.Item) bool {
		// This visitor callback will be invoked with every item
		// with key "ford" and onwards, in key-sorted order.
		// So: "mercedes", "tesla" are visited, in that ascending order,
		// but not "bmw".
		// If we want to stop visiting, return false;
		// otherwise return true to keep visiting.
		return true
	})

	// Let's get a snapshot.
	snap := s.Snapshot()
	snapCars := snap.GetCollection("cars")

	// The snapshot won't see modifications against the original Store.
	c.Delete([]byte("mercedes"))
	mercedesIsNil, err := c.Get([]byte("mercedes"))
	HandleError(err)
	fmt.Println(mercedesIsNil)
	mercedesPriceFromSnapshot, err := snapCars.Get([]byte("mercedes"))
	HandleError(err)
	fmt.Println(mercedesPriceFromSnapshot)

	// Persist all the changes to disk.
	s.Flush()

	f.Sync() // Some applications may also want to fsync the underlying file.

	// Now, other file readers can see the data, too.
	f2, err := os.Open("/tmp/test.gkvlite")
	HandleError(err)
	s2, err := gkvlite.NewStore(f2)
	HandleError(err)
	c2 := s2.GetCollection("cars")

	bmwPrice, err := c2.Get([]byte("bmw"))
	HandleError(err)
	fmt.Println(bmwPrice)
}
