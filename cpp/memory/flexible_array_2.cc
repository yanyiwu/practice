#include <iostream>
#include <malloc.h>
#include <assert.h>
#include <stdio.h>
#include <vector>
#include <cstdlib>

using namespace std;

struct NodeA {
  size_t level;
  size_t number[1];
};

const size_t N =  1L*256*1024*1024;

NodeA* NewNodeA() {
  NodeA* node = (NodeA*)malloc(sizeof(NodeA) + N * sizeof(size_t));
  assert(node != NULL);
  for (size_t i = 0; i < N; i++) {
    node->number[i] = i;
  }
  return node;
}

void test1() {
  NodeA* node = NewNodeA();
  assert(node != NULL);
  size_t r = rand() % N;
  cout << __FILE__ << __LINE__ << endl;
  cout << node->number[r] << endl;
  free(node);
}

int main() {
  //for (size_t i = 0; i < 1000; i++) {
  test1();
  //}
  getchar();
  return 0;
}

