/*
  Darts -- Double-ARray Trie System

  $Id: darts.cpp 1674 2008-03-22 11:21:34Z taku $;

  Copyright(C) 2001-2007 Taku Kudo <taku@chasen.org>
  All rights reserved.
*/
#include "darts.h"
#include <iostream>
#include <string>

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " Index" << std::endl;
    return -1;
  }

  Darts::DoubleArray da;
  std::string index = argv[argc-1];

  if (da.open(index.c_str())) {
    std::cerr << "Error: cannot open " << index << std::endl;
    return -1;
  }

  Darts::DoubleArray::result_pair_type  result_pair[1024];
  Darts::DoubleArray::key_type          key[1024];

  while (std::cin.getline(key, sizeof(key))) {
    size_t num = da.commonPrefixSearch(key, result_pair, sizeof(result_pair));
    if (num == 0) {
      std::cout << key << ": not found" << std::endl;
    } else {
      std::cout << key << ": found, num=" << num << " ";
      for (size_t i = 0; i < num; ++i) {
        std::cout << " " << result_pair[i].value
                  << ":" << result_pair[i].length;
      }
      std::cout << std::endl;
    }
  }

  return 0;
}
