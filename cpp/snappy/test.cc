#include <iostream>
#include <deque>
#include <snappy.h>
#include <fstream>

using namespace std;

int main(int argc, char** argv) {
  if (argc < 2) {
    cout << "usage: " << argv[0] << " <filename>" << endl;
    return -1;
  }
  ifstream ifs(argv[1]);
  string x;
  size_t total_input_size = 0;
  size_t total_output_size = 0;
  while (getline(ifs, x)) {
    string y;
    snappy::Compress(x.data(), x.size(), &y);
    total_input_size += x.size();
    total_output_size += y.size();
  }
  cout << "total_input_size: " << total_input_size << endl;
  cout << "total_output_size: " << total_output_size << endl;
  return 0;
}
