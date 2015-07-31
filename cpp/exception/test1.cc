#include <exception>
#include <iostream>

using namespace std;

void funct() throw() {
  cout << "hello throw" << endl;
  // throw() is only a GentleMan's Agreement, so you still can throw exception in it and compiler woulld not complain anything.
  throw 4;
}

int main() {
  funct();
  return 0;
}
