#include <iostream>

using namespace std;

class A {
 public:
  static void Fun() {
      cout << "Fun" << endl;
  }
};



int main() {
  A::Fun();
  A *a = NULL;
  a->Fun();
  return 0;
}

