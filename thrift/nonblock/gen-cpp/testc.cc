#include <stdlib.h>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <boost/smart_ptr.hpp>
#include <transport/TSocket.h>
#include <transport/TBufferTransports.h>
#include <protocol/TBinaryProtocol.h>
#include "tests.h"

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using boost::shared_ptr;

int main(int argc, char* argv[]) {

  shared_ptr<TSocket> socket(new TSocket("0.0.0.0", 11240));
  shared_ptr<TTransport> transport(new TBufferedTransport(socket));
  shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
  shared_ptr<testsClient> client(new testsClient(protocol));

  transport->open();
  
  transport->close(); 
  return 0;
}
