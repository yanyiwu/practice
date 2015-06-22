// bad_alloc example
#include <iostream>     // std::cout
#include <new>          // std::bad_alloc
#include <vector>

int main () {
  try
  {
    std::vector<int> a(1000000000000);
  }
  catch (std::bad_alloc& ba)
  {
    std::cerr << "bad_alloc caught: " << ba.what() << '\n';
  }
  return 0;
}
