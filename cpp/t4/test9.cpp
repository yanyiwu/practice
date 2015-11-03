#include <iostream>
#include <vector>

using namespace std;

class A {
 public:
  A() {
    cout << "A" << endl;
  }  
  ~A() {
    cout << "~A" << endl;
  }  
}; 
class B {
 public:
  B() {
    cout << "B" << endl;
  }  
  ~B() {
    cout << "~B" << endl;
  }  
}; 

class X {
 public:
  A a;
  B b;
}; 

int main() {
  X x;
  return 0;
}

