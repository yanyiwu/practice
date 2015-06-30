#include <iostream>
#include <malloc.h>
#include <assert.h>
#include <stdio.h>
#include <vector>
#include <cstdlib>

using namespace std;

struct NodeA {
  size_t level;
  NodeA* b[1];
};

const size_t N =  1L*1024*1024*1024;

void test1() {
  NodeA* node = (NodeA*)malloc(sizeof(NodeA) + N * sizeof(NodeA*));
  assert(node != NULL);
  size_t r = rand() % N;
  cout << __FILE__ << __LINE__ << endl;
  cout << ((char*)node)[r] << endl;
  free(node);
  //getchar();
}

int main() {
  for (size_t i = 0; i < 1000; i++) {
    test1();
  }
  getchar();
  return 0;
}
