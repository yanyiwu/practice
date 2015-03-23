#include <iostream>
#include <vector>

using namespace std;

class A {
 public:
  A() {
  }
  A(int a, int b) : a_(a), b_(b) {
  }
  int a_;
  int b_;
};

int main() {
  vector<A> va;
  va.push_back(A(1, 2));
  va.push_back(A(2, 3));

  cout << va.size() << endl;
  va.resize(1);
  cout << va.size() << endl;
  cout << va[0].a_ << endl;
  cout << va[0].b_ << endl;
  return 0;
}
