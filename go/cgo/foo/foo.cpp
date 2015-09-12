#include <iostream>
#include "foo.hpp"

void
cxxFoo::Bar() {
  std::cout << this->a << std::endl;
}
