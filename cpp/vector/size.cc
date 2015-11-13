#include <iostream>
#include <vector>

using namespace std;

int main() {
  vector<int> vec;
  vec.push_back(1);
  for (size_t i = 0; i < vec.size(); i++) {
    vec.push_back(i);
    cout << i << endl;
  }
  return 0;
}
