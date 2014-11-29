#include <boost/bind.hpp>   
#include <boost/function.hpp>
#include <string>
#include <iostream>

using namespace boost;
using namespace std;

void fun1(const char* s1, const char* s2) {
    cout << __FILE__ << __LINE__ << endl;
    cout << s1 << endl;
    cout << s2 << endl;
    cout << __FILE__ << __LINE__ << endl;
}

int main() {
    boost::function<void (const char*)> fn;
    char * s1 = (char*)malloc(3);
    s1[0] = 's';
    s1[1] = '1';
    s1[2] = '\0';
    fn = bind(fun1, s1, _1);
    cout<<__FILE__ <<__LINE__<<endl;
    s1[1]='3';
    free(s1);
    cout << s1 << endl;
    cout<<__FILE__ <<__LINE__<<endl;
    fn("s2");
    return 0;
}
