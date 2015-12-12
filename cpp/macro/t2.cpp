#include <iostream>
using namespace std;

#define XXX(x) {cout << x << endl;}

#ifdef XXX
#warning "warning"
#endif

#ifdef XXX
#error "error"
#endif // XXX

int main()
{
    return 0;
}
