#include <iostream>
#include <deque>
#include <stdio.h>

using namespace std;

class X {
 public:
  X(): number(1) {
    cout << "X()" << endl;;
  }
  ~X() {
    cout << "~X()" << endl;
  }
  int number;
};

int main() {
  deque<X> dq;
  X x1;
  x1.number = 0;
  dq.push_back(x1);
  dq.resize(5);
  for (size_t i = 0; i < dq.size(); i++) {
    cout << dq[i].number << endl;
  }
  getchar();
  dq.resize(1);
  for (size_t i = 0; i < dq.size(); i++) {
    cout << dq[i].number << endl;
  }
  getchar();
  return 0;
}
