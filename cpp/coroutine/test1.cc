#include <iostream>
#include <ucontext.h>

using namespace std;

typedef void (*Function)(void* arg);

ucontext_t ucp;

void Foo(void* arg) {
  cout << "Foo Begin" << endl;
  getcontext(&ucp);
  cout << "Foo End" << endl;
}

void Bar(void* arg) {
  cout << "Bar Begin" << endl;
  setcontext(&ucp);
  cout << "Bar End" << endl;
}

int main() {
  Foo(NULL);
  Bar(NULL);
  return 0;
}
