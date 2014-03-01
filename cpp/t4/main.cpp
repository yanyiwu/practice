#include <iostream>
#define NDEBUG
#include <cassert>

using namespace std;
bool funct(bool in)
{
    cout<< in << endl;
    return in;
}
int main()
{
    assert(funct(false));
    return 0;
}
