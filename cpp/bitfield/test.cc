#include <iostream>
#include <stdint.h>

using namespace std;

struct S1 {
  uint32_t a;
  bool b;
};

struct S2 {
  uint32_t a : 31;
  bool b: 1;
};

struct S3 {
  uint32_t a : 31;
  uint32_t b: 1;
};

int main() {
  cout << sizeof(S1) << endl;
  cout << sizeof(S2) << endl;
  cout << sizeof(S3) << endl;
  S3 s;
  s.a = 10;
  s.b = 300;
  cout << s.a << endl;
  cout << s.b << endl;
  cout << bool(s.b) << endl;
  s.b = 1;
  cout << bool(s.b) << endl;
  return 0;
}
