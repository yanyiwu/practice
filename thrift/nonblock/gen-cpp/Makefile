all: server client
server:
	g++ -o testserver -DHAVE_NETINET_IN_H -I/usr/local/include/thrift/ -I/usr/local/include/ tests_constants.cpp tests_server.skeleton.cpp  tests_types.cpp tests.cpp -L/usr/local/lib -lthrift
client:
	g++ -o testclient -DHAVE_NETINET_IN_H -I/usr/local/include/thrift/ -I/usr/local/include/ tests_constants.cpp  testc.cc  tests_types.cpp tests.cpp -L/usr/local/lib -lthrift
