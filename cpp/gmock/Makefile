all:
	g++ -c -I../gtest/gtest-1.6.0/include/ -I./gmock/ -I./gmock/include/ ./gmock/src/gmock-all.cc
	ar rv libgmock.a gmock-all.o
	g++ -c -I../gtest/gtest-1.6.0/include/ -I../gtest/gtest-1.6.0 -I../gtest/gtest-1.6.0/include ../gtest/gtest-1.6.0/src/gtest-all.cc
	ar rv libgtest.a gtest-all.o
	g++ -c -I../gtest/gtest-1.6.0/include/ -I./gmock/include foo_test.cc gtest_main.cc
	g++ -o gmock_test gtest_main.o foo_test.o -L./ -lgmock -lgtest -lpthread
debug:
	g++ -c -I../gtest/gtest-1.6.0/include/ -I./gmock/include foo_test.cc gtest_main.cc
	g++ -o gmock_test gtest_main.o foo_test.o -L./ -lgmock -lgtest -lpthread
test:
	./gmock_test
clean:
	rm -f *.a *.o gmock_test
