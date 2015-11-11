#include <iostream>
using namespace std;

int main() {
#if __cplusplus >= 201103L
#error __cplusplus >= 201103L
#elif __cplusplus <= 199711L 
#error __cplusplus <= 199711L
#else 
#error __cplusplus
#endif
  return 0;
}
