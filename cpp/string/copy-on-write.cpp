#include <iostream>
#include <map>
#include <string>
#include <cassert>

using namespace std;

void Test1() {
  string x = "1234567";
  map<string, int> mp;
  cout << __FILE__ << __LINE__ << endl;
  cout << x << " " << x.size() << endl;
  cout << mp.insert(make_pair(x, 1)).second << endl;
  //char* p = (char*)x.c_str();
  //p[1] = '3';
  x[1]='3';
  //cout << __FILE__ << __LINE__ << endl;
  //cout << x << " " << x.size() << endl;
  //cout << mp.insert(make_pair(x, 1)).second << endl;

  cout << __FILE__ << __LINE__ << endl;
  for (map<string, int>::const_iterator iter = mp.begin(); iter != mp.end(); ++iter) {
    cout << iter->first << endl;
  }
  cout << mp.size() << endl;
}

void Test2() {
}

int main() {
  Test1();
  return 0;
}
