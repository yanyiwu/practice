// bad_alloc example
#include <iostream>     // std::cout
#include <new>          // std::bad_alloc
#include <vector>
#include <exception>

class MyException: public std::exception {  
 public:  
  MyException(size_t n): size_(n) {  
  }  
  virtual const char* what() const throw() {
    return "my exception";
  }
  size_t Size() const {
    return size_;
  }
 private:
  size_t size_;
}; 

void Test() {
  std::vector<int> v(5);
  try {
    v.resize(1000000000000);
  } catch (std::bad_alloc& ba) {
    throw MyException(v.size());
    std::cerr << "bad_alloc caught: " << ba.what() << std::endl;
  }
}

int main () {
  try {
    Test();
  } 
  catch (MyException& e) {
    std::cerr << e.what() << std::endl;
    std::cerr << e.Size() << std::endl;
  }
  return 0;
}

