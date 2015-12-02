#include <iostream>

using namespace std;

class Foo {
 public:
  Foo(int y): y_(y) {
  }

  void Cout(int x) {
    cout << "Foo::Cout x: " << x  << " ,y: " << y_ << endl;
  }
  void Cout2(int x) {
    cout << "Foo::Cout2 x: " << x  << " ,y: " << y_ << endl;
  }
  
  int y_;
};

void Print(int x) {
  cout << "Print" << x << endl;
}

void Run(int x, void(*f)(int)) {
  (*f)(x);
}

void RunC(int x, Foo* obj, void(Foo::*f)(int)) {
  (obj->*f)(x);
}

int main() {
  Run(1, &Print);
  Foo obj(11);
  RunC(2, &obj, &Foo::Cout);
  RunC(2, &obj, &Foo::Cout2);
  return 0;
}
