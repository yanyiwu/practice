#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <string>
#include <exception>

using namespace std;

static const float EPSILON = 1e-6f;

int main() {
  float x = 1.0f;
  float y = 0.0f;
  float z = x / y;
  float w = z*10;
  cout << z << endl;
  cout << w << endl;
  cout << 1/float(0) << endl;
  cout << 1.0/0 << endl;
  cout << 0.01/EPSILON << endl;
  try {
    cout << 1/0 << endl; // crash
  } catch(std::exception& e) {
    cout << e.what() << endl;
  } catch(...) {
    cout << "something wrong" << endl;
  }
  return 0;
}

