#include <iostream>
#include <map>
#include <boost/smart_ptr.hpp>

using namespace std;
using namespace boost;

class X {
 public:
  X() {
  }
  ~X() {
    cout << __FILE__ << __LINE__ << endl;
  }
};

class XFactory {
 public:
  shared_ptr<X> Get(const string& name) {
    return mp_[name];
  }
 private:
  map<string, shared_ptr<X> > mp_; 
};

void Func() {
  XFactory factory;
  shared_ptr<X> x = factory.Get("yanyiwu");
  x.reset(new X());
}

int main() {
  Func();
  return 0;
}
