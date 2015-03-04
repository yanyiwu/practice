#include <iostream>
using namespace std;

int ga;

void print(int a = ga) {
  cout << a << endl;
}

int main() {
  print();
  ga = 1;
  print();
  return 0;
}
