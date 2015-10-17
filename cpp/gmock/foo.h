#ifndef FOO_H
#define FOO_H

#include "bob.h"

class Foo {
 public:
  Foo(BobInterface* bob): bob_(bob) {
  }
  ~Foo() {
  }
  int Add(int x, int y, int z) {
    return bob_->Add(bob_->Add(x, y), z);
  }
 private:
  BobInterface* bob_;
}; // class Foo

#endif // FOO_H
