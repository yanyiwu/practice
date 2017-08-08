#include <iostream>
#include <stdint.h>
#include <Eigen/Dense>  
//#include "./repos/cpp3rdlib/Eigen/Dense"
using namespace Eigen;  
typedef Matrix<double, Dynamic, Dynamic> C;
int main()  
{  
  C m(2,2);  
  m(0,0) = 3;  
  m(1,0) = 2.5;  
  m(0,1) = -1;  
  m(1,1) = m(1,0) + m(0,1);  
  m.resize(2,2);
  std::cout << m.rightCols(1) << std::endl;
  std::cout << m.leftCols(1) << std::endl;
  std::cout << "Here is the matrix m:\n" << m << std::endl;  
}  

