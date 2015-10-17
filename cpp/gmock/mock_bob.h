#ifndef MOCK_BOB_H
#define MOCK_BOB_H

#include "bob_interface.h"
#include "gmock/gmock.h"

class MockBob: public BobInterface {
 public:
  MOCK_METHOD2(Add, int(int x, int y));
}; // class MockBob

#endif // MOCK_BOB_H
