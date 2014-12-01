#include <boost/bind.hpp>   
#include <boost/function.hpp>
#include <string>
#include <iostream>

using namespace boost;
using namespace std;

class mystr {
    public:
        mystr()
        {
        }
        mystr(const char* cstr)
        {
            str_ = cstr;
        }
        ~mystr()
        {
        }
        mystr(const mystr& mystr) 
        {
            cout << __FILE__ << __LINE__ << endl;
            cout << "mystr" << endl;
            str_ = mystr.str_;
        }
        mystr& operator = (const mystr& mystr)
        {
            cout << __FILE__ << __LINE__ << endl;
            cout << "operator=" << endl;
            str_ = mystr.str_;
            return *this;
        }
        char& operator [] (size_t idx) 
        {
            return str_[idx];
        }
        string str_;
};

ostream & operator<< (ostream& os, const mystr& str) 
{
    return os << str.str_;
}

void fun1(const string& s1, const string& s2) {
    cout << __FILE__ << __LINE__ << endl;
    cout << s1 << endl;
    cout << s2 << endl;
    cout << __FILE__ << __LINE__ << endl;
}
void fun2(const mystr& s1, const mystr& s2) {
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


void test3() {
    boost::function<void (const string&)> fn;
    string s1("s1");
    int i1 = 0;
    int i2 = 1;
    fn = bind(fun1, s1, _1);
    cout<<__FILE__ <<__LINE__<<endl;
    s1[1]='3';
    cout << s1 << endl;
    cout<<__FILE__ <<__LINE__<<endl;
    fn("s2");
}

void test4() {
    boost::function<void (const mystr&)> fn;
    mystr s1("s1");
    int i1 = 0;
    int i2 = 1;
    fn = bind(fun2, s1, _1);
    //cout<<__FILE__ <<__LINE__<<endl;
    s1[1]='3';
    //cout << s1 << endl;
    //cout<<__FILE__ <<__LINE__<<endl;
    fn("s2");
}

int main() {
    //test1();
    //test2();
    //test3();
    test4();
    return 0;
}
