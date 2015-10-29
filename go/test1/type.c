#include <stdio.h>

// x是数组，数组的元素是指针，指针的指向是数组，数组的元素是指针，指针指向的是int
int*(*x[5])[5];


int main() {
  int i = 10;
  int* ii[5];
  ii[0] = &i;
  x[0]=&ii;
  printf("%d\n", *(*x[0])[0]);
  return 0;
}
