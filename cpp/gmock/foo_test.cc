#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "foo.h"
#include "bob.h"
#include "mock_bob.h"

TEST(FooTest, Test1) {
  MockBob mockBob;
  BobInterface* bob = &mockBob;
  Foo foo(bob);
  EXPECT_CALL(mockBob, Add(1, 2))\
    .Times(::testing::Exactly(1))\
    .WillOnce(::testing::Return(3));

  EXPECT_CALL(mockBob, Add(3, 3))\
    .Times(::testing::Exactly(1))\
    .WillOnce(::testing::Return(6));

  EXPECT_EQ(6, foo.Add(1, 2, 3));
}
