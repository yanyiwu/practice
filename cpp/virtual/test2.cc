#include <iostream>

using namespace std;

class A {
 public:
  virtual ~A() {
    cout << "~A" << endl;
  }
  virtual void F() const = 0;
};

class B: public A {
 public:
  virtual ~B() {
    cout << "~B" << endl;
  }
  void F() {
    cout << "B F()" << endl;
  }
};

int main() {
  A* a = new B();
  a->F();
  delete a;
  return 0;
}
