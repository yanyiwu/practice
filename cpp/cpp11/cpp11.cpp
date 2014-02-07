#include <iostream>
#include <vector>
#include <string>

using namespace std;

template <class T>
    void print2(T x)
    {
        for(auto y: x){cout<<y<<endl;}
    }

//#define print(x) for(auto y : x) {cout << y << endl;};
#define print(x) for(const auto & y : x) {cout << y << endl;};

int main()
{
    auto i = 1;
    const char *a[] = {"111", "222", "333"};
    vector<string> b = {"111", "222", "333"};
    print2(b);
    print(b);
    return 0;
}
