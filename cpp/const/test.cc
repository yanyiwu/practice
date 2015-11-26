#include <iostream>
using namespace std;

class X {
 public:
  X(int* const a): x_(a) {
  }
  void Funct() const {
    (*x_) = 1;
    // x_ = NULL; // compile error
  }

  int* x_;
};

int main() {
  int a = 0;
  X x(&a);
  cout << x.x_ << endl;
  cout << (*x.x_) << endl;
  x.Funct();
  cout << x.x_ << endl;
  cout << (*x.x_) << endl;

  cout << a << endl;
  return 0;
}
