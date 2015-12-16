#include "limonp/ThreadPool.hpp"
#include "limonp/StdExtension.hpp"
#include <unistd.h> // for function: usleep

using namespace std;

const size_t THREAD_NUM = 4;

class Foo {
 public:
  void Append(char c) {
    limonp::MutexLockGuard lock(mutex_);
    chars.push_back(c);
    usleep(10*1000); // just for make chars more disorder
  }

  string chars;
  limonp::MutexLock mutex_;
};

void DemoClassFunction() {
  Foo foo;
  cout << foo.chars << endl;
  limonp::ThreadPool thread_pool(THREAD_NUM);
  thread_pool.Start();
  for (size_t i = 0; i < 20; i++) {
    char c = i % 10 + '0';
    thread_pool.Add(limonp::NewClosure(&foo, &Foo::Append, c));
  }
  thread_pool.Stop();
  cout << foo.chars << endl;
}

int main() {
  DemoClassFunction();
  return 0;
}
