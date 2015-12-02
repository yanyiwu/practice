#include <iostream>

using namespace std;

class Foo {
 public:
  Foo() {
  }

  void Cout(int x) {
    cout << "Foo::Cout" << x << endl;
  }
};

void Print(int x) {
  cout << "Print" << x << endl;
}

typedef void(*FT)(int);

void Run(int x, FT f) {
  (*f)(x);
}

typedef void(Foo::* CFT)(int);

void RunC(int x, Foo* obj, CFT f) {
  (obj->*f)(x);
}

int main() {
  Run(1, &Print);
  Foo obj;
  RunC(2, &obj, &Foo::Cout);
  return 0;
}

