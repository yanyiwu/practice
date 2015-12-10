#include <iostream>
#include <fstream>
#include <algorithm>
#include <map>
#include <string>

using namespace std;

class Foo {
 public:
  Foo(int x): x_(x) {
    cout << "Foo()" << x_ << endl;
  }
  ~Foo() {
    cout << "~Foo()" << x_ << endl;
  }
 private:
  int x_;
};

void Test1() {
  Foo foo1(1);
  Foo foo2(2);
}

void Test2() {
  Foo(1);
  Foo(2);
}

int main() {
  Test1();
  Test2();
  return 0;
}

