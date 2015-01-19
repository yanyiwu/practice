#include <iostream>
using namespace std;


template<typename T>
void Print(const T& a, const T& b) {
  cout << a << "," << b << endl;
}

template<>
void Print(const int& a, const int& b) {
  cout << a << "+" << b << endl;
}

int main() {
  Print("12","23");
  Print(12,23);
  return 0;
}
