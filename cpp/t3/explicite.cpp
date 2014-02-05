#include <iostream>
using namespace std;
class A
{
    public:
        explicit A(int i){};
};
int main()
{
    A a = 1;// if not explicit, this line compile ok.
    return 0;
}
