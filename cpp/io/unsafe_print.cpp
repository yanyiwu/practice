#include <iostream>

using namespace std;

void print(const char* str) {
  printf(str);
}

int main() {
  const char* str = NULL;
  print("hello\n"); //ok
  print("%s");// segment fault
  return 0;
}
