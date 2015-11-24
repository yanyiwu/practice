#include <iostream>
#include <boost/smart_ptr.hpp>

using namespace std;
using namespace boost;

int main() {
  boost::shared_ptr<const int> x(new int(1024));
  //*x = 12580; // compile failed.
  cout << *x << endl;
  return 0;
}
