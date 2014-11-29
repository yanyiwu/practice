#include <boost/bind.hpp>   
#include <boost/function.hpp>
#include <string>
#include <iostream>

using namespace boost;
using namespace std;

void fun1(const string& s1, const string& s2) {
    cout << __FILE__ << __LINE__ << endl;
    cout << s1 << endl;
    cout << s2 << endl;
    cout << __FILE__ << __LINE__ << endl;
}

void test1() {
    boost::function<void (const string&)> fn;
    string * s1 = new string("s1");
    fn = bind(fun1, *s1, _1);
    cout<<__FILE__ <<__LINE__<<endl;
    (*s1)[1]='3';
    cout << (*s1) << endl;
    cout<<__FILE__ <<__LINE__<<endl;
    fn("s2");
}

void test2() {
    boost::function<void (const string&)> fn;
    string * s1 = new string("s1");
    fn = bind(fun1,boost::ref(*s1), _1);
    cout<<__FILE__ <<__LINE__<<endl;
    (*s1)[1]='3';
    cout << (*s1) << endl;
    cout<<__FILE__ <<__LINE__<<endl;
    fn("s2");
}

int main() {
    test1();
    test2();
    return 0;
}
