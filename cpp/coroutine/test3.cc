#include <iostream>
#include <ucontext.h>

using namespace std;

typedef void (*Function)(void* arg);

const size_t STACK_SIZE = 1024*1024;
char stack[STACK_SIZE];

ucontext_t ucp;
ucontext_t ucp2;

void Foo() {
  cout << "Foo Begin" << endl;
  getcontext(&ucp);
  cout << "Foo End" << endl;
}

void Tom() {
  cout << "Tom Begin" << endl;
  swapcontext(&ucp2, &ucp);
  cout << "Tom End" << endl;
}

void Jim() {
  cout << "Jim Begin" << endl;
  cout << "Jim End" << endl;
}

int main() {
  Foo();
  ucp.uc_stack.ss_sp = stack;
  ucp.uc_stack.ss_size = sizeof(stack)/sizeof(*stack);
  ucp.uc_link = &ucp2;
  makecontext(&ucp, &Jim, 0);
  Tom();
  cout << "main exit" << endl;
  return 0;
}
