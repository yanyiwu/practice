#include <iostream>
#include <string>
#include <sstream>
using namespace std;

class A {
 public:
  A() {
  }
  const string& Get() const {
    return emptystr_;
  }
 private:
  const string emptystr_;
};

int main() {
  A ca;
  const string& a = ca.Get();
  cout << a << endl;
  cout << a.empty() << endl;

  string s;
  stringstream ss;
  ss << 1;
  ss.str(s);
  ss.clear();
  cout << s << endl;
  cout << ss.str() << endl;
  
  return 0;
}
