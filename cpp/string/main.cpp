#include <iostream>
#include <string>
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
  return 0;
}
