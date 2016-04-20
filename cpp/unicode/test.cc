#include "unicode.h"
#include <iostream>

using namespace unicode;
using namespace std;

int main() {
  const char* s = "你好世界hello world"; 
  size_t len = strlen(s);
  vector<RuneStr> runes;
  DecodeRunesInString(s, len, runes);
  for (size_t i = 0; i < runes.size(); i++) {
    cout << runes[i].str - s << " " << string(runes[i].str, runes[i].len) << endl;
  }
  return 0;
}
