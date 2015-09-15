#include <iostream>

using namespace std;

struct Foo {
  int x;
};

struct Bar: public Foo {
  int y;
};

int main() {
  cout << sizeof(Foo) << endl;
  cout << sizeof(Bar) << endl;
  return 0;
}
