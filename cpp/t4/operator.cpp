#include <iostream>
using namespace std;

struct Item {
  int a;
  int b;
};

class A {
 public:
  A(int i) {
    item.a = i;
  }
  Item* operator -> () {
    return &item;
  } 
  Item operator * () {
    return item;
  }
 private:
  Item item;
};

int main() {
  A ca(1);
  cout << (*ca).a << endl;
  cout << ca->a << endl;
  return 0;
}
