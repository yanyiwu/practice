#include <iostream>
#include <map>
#include <boost/smart_ptr.hpp>
#include <boost/make_shared.hpp>

using namespace std;
using namespace boost;

class A {
 public:
  A(int a): m_a(a) {
  }
  ~A() {
    cout << __FILE__ << __LINE__ << endl;
  }
  int m_a;
};

int main() {
  shared_ptr<A> a(new A(1));
  shared_ptr<A> b(a);
  shared_ptr<A> c(a);
  cout << a->m_a << endl;
  cout << b->m_a << endl;
  cout << c->m_a << endl;
  c.reset(new A(2));
  cout << a->m_a << endl;
  cout << b->m_a << endl;
  cout << c->m_a << endl;
  return 0;
}
