#include <iostream>
using namespace std;

class A {
 public:
  A(): count_(*(int*)(NULL)) {
  }
 private:
  int& count_;
};

int main() {
  A a;
  return 0;
}

