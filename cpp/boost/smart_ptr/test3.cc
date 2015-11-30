#include <iostream>
#include <map>
#include <boost/smart_ptr.hpp>

using namespace std;
using namespace boost;

class A {
 public:
  A() {
  }
  ~A() {
    cout << __FILE__ << __LINE__ << endl;
  }
  shared_ptr<class B> m_b;
};

class B {
 public:
  B() {
  }
  ~B() {
    cout << __FILE__ << __LINE__ << endl;
  }
  shared_ptr<A> m_a;
};

int main() {
  while(true) {
    shared_ptr<A> a(new A);
    shared_ptr<B> b(new B);
    a->m_b = b;
    b->m_a = a;
  }
  return 0;
}
