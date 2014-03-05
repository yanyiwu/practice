#include <iostream>
using namespace std;
#define GTEST_TEST_CLASS_NAME_(test_case_name, test_name) test_case_name##_##test_name##_Test
#define COMMAND(line) #line
#define print(x) cout << #x": " << x << endl; 
int main()
{
    int x1 = 1;
    print(x1);
    cout<< COMMAND(GTEST_TEST_CLASS_NAME_(name1, name2)) << endl;
    return 0;
}
