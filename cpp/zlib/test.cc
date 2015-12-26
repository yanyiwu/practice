#include <iostream>
#include <sstream>
#include <fstream>
#include <deque>
#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filter/zlib.hpp>

using namespace std;

string CompressData(const string &data)
{
    stringstream compressed;
    stringstream decompressed;
    decompressed << data;
    boost::iostreams::filtering_streambuf<boost::iostreams::input> out;
    out.push(boost::iostreams::zlib_compressor());
    out.push(decompressed);
    boost::iostreams::copy(out, compressed);
    return compressed.str();
}

string DecompressData(const string &data)
{
    stringstream compressed;
    stringstream decompressed;
    compressed << data;
    boost::iostreams::filtering_streambuf<boost::iostreams::input> in;
    in.push(boost::iostreams::zlib_decompressor());
    in.push(compressed);
    boost::iostreams::copy(in, decompressed);
    return decompressed.str();
}

const size_t N = 1;

int main(int argc, char** argv) {
  deque<string> ss;
  if (argc < 2) {
    cout << "usage: " << argv[0] << " <filename>" << endl;
    return -1;
  }
  for (size_t i = 0; i < N; i++) {
    ifstream ifs(argv[1]);
    string original;
    while (getline(ifs, original)) {
      //cout << original.size() << endl;
      //string compressed = CompressData(original);
      //cout << compressed.size() << endl;
      //string decompressed = DecompressData(compressed);
      //cout << decompressed.size() << endl;
      //getchar();
      //ss.push_back(y);
    }
  }
  return 0;
}
