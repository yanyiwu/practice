#include <iostream>

using namespace std;

class A {
 private:
  int a_;
  friend class B;
};

class B {
 public:
  void Print() {
    A ca;
    cout << ca.a_ << endl;
  }
};

int main() {
  B b;
  b.Print();
  return 0;
}
