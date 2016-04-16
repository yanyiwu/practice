#include <stdint.h>
#include <stdlib.h>
#include <vector>

namespace unicode {

struct RuneStr {
  uint32_t rune;
  const char* str;
  uint32_t len;
}; // struct RuneStr

struct RuneStrLite {
  uint32_t rune;
  uint32_t len;
}; // struct RuneStrLite

RuneStrLite DecodeRuneInString(const char* str, size_t len);

bool DecodeRunesInString(const char* s, size_t len, std::vector<RuneStr>& runes) {
  runes.reserve(len / 2);
  for (size_t i = 0; i < len;) {
    RuneStrLite rp = DecodeRuneInString(s + i, len - i);
    if (rp.len == 0) {
      return false;
    }
    RuneStr x = {rp.rune, s + i, rp.len};
    runes.push_back(x);
    i += rp.len;
  }
  return true;
}

RuneStrLite DecodeRuneInString(const char* str, size_t len) {
  RuneStrLite rp = {0, 0};
  if (str == NULL || len == 0) {
    return rp;
  }
  if (!(str[0] & 0x80)) { // 0xxxxxxx
    // 7bit, total 7bit
    rp.rune = (uint8_t)(str[0]) & 0x7f;
    rp.len = 1;
  } else if ((uint8_t)str[0] <= 0xdf &&  1 < len) { 
    // 110xxxxxx
    // 5bit, total 5bit
    rp.rune = (uint8_t)(str[0]) & 0x1f;

    // 6bit, total 11bit
    rp.rune <<= 6;
    rp.rune |= (uint8_t)(str[1]) & 0x3f;
    rp.len = 2;
  } else if((uint8_t)str[0] <= 0xef && 2 < len) { // 1110xxxxxx
    // 4bit, total 4bit
    rp.rune = (uint8_t)(str[0]) & 0x0f;

    // 6bit, total 10bit
    rp.rune <<= 6;
    rp.rune |= (uint8_t)(str[1]) & 0x3f;

    // 6bit, total 16bit
    rp.rune <<= 6;
    rp.rune |= (uint8_t)(str[2]) & 0x3f;

    rp.len = 3;
  } else if((uint8_t)str[0] <= 0xf7 && 3 < len) { // 11110xxxx
    // 3bit, total 3bit
    rp.rune = (uint8_t)(str[0]) & 0x07;

    // 6bit, total 9bit
    rp.rune <<= 6;
    rp.rune |= (uint8_t)(str[1]) & 0x3f;

    // 6bit, total 15bit
    rp.rune <<= 6;
    rp.rune |= (uint8_t)(str[2]) & 0x3f;

    // 6bit, total 21bit
    rp.rune <<= 6;
    rp.rune |= (uint8_t)(str[3]) & 0x3f;

    rp.len = 4;
  } else {
    rp.rune = 0;
    rp.len = 0;
  }
  return rp;
}

} // namespace
