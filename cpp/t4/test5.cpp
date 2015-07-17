#include <iostream>
#include <algorithm>
#include <map>
#include <string>

using namespace std;

void test1() {
  map<int, double> mp;
  mp[1] = 2.0;
  mp[2] = 1.0;
  double x = max_element(mp.begin(), mp.end())->second;
  cout << x << endl;
}

void test2() {
  map<int, double> mp;
  double x = max_element(mp.begin(), mp.end())->second;
  cout << x << endl;
}

int main() {
  test1();
  test2();
  return 0;
}

