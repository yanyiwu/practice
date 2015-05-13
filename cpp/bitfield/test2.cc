#include <iostream>
#include <memory.h>
using namespace std;
struct A
{
    int a:5;
    int b:3;
};
int main(void)
{
    char str[100] = "0";
        struct A d;
    memcpy(&d, str, sizeof(A));
    cout << d.a << endl;
    cout << d.b << endl;
    cout << int('0') << endl;
    return 0;
}
