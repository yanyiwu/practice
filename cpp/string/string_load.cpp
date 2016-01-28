#include <iostream>
#include <fstream>
#include <cassert>

using namespace std;

void Load(string& s, size_t offset, size_t size) {
  s.resize(size);
  FILE* fp = fopen("testdata1", "r");
  assert(fp != NULL);
  fseek(fp, offset, SEEK_SET);
  fread((char*)s.c_str(), sizeof(char), size, fp);
  fclose(fp);
}

int main() {
  string s;
  Load(s, 0, 3);
  cout << s << endl;
  assert(s == "123");

  string s2 = s;
  Load(s2, 1, 3);
  cout << s2 << endl;
  assert(s2 == "234");
  cout << s << endl;
  assert(s == "123");
  return 0;
}
