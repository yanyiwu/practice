#include <iostream>
using namespace std;
#define GTEST_TEST_CLASS_NAME_(test_case_name, test_name) test_case_name##_##test_name##_Test
#define COMMAND(line) #line
#define print(x) cout << #x": " << x << endl; 

#define CREATE_BRICK_SOURCE(NAME, TPL_BRICK, CONTEXT, NEXT_BRICK) \
typedef TPL_BRICK<TYPEOF(CONTEXT), TYPEOF(*NEXT_BRICK)> __C_##NAME;                     \
typedef __C_##NAME *__S_##NAME;                                                         \
               __S_##NAME NAME(aligned_new(__C_##NAME, CONTEXT, NEXT_BRICK)); 
int main()
{
    int x1 = 1;
    print(x1);
    cout<< COMMAND(GTEST_TEST_CLASS_NAME_(name1, name2)) << endl;
    return 0;
}
