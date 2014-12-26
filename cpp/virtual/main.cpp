#include <iostream>

using namespace std;

class A1 {
    public:
        virtual void func1() {};
};

class B1 : public A1 {
    public:
        virtual void func2() {};
};

class A2 {
    public:
        virtual void func1() {};
};

class B2 : public virtual A2 {
    public:
        virtual void func2() {};
};
class A3 {
    public:
        virtual void func1() {};
        char x;
};

class B3 : public virtual A3 {
    public:
        virtual void func3() {};
};

class A4 {
    public:
        virtual void func1() {};
        char x;
};

class B4 : virtual A4 {
    public:
        virtual void func4() {};
};

class A5 {
    char x[64];
};
class B51: public A5 {
    
};
class B52: public A5 {
};
class C5: public B51, public B52 {
};
class B53: virtual public A5 {
    
};
class B54: virtual public A5 {
};
class C52: public B53, public B54 {
};

int main() {
    cout << sizeof(A1) << endl;
    cout << sizeof(B1) << endl;
    cout << endl;
    cout << sizeof(A2) << endl;
    cout << sizeof(B2) << endl;
    cout << endl;
    cout << sizeof(A3) << endl;
    cout << sizeof(B3) << endl;
    cout << endl;
    cout << sizeof(A4) << endl;
    cout << sizeof(B4) << endl;
    cout << endl;
    cout << sizeof(A5) << endl;
    cout << sizeof(B51) << endl;
    cout << sizeof(B52) << endl;
    cout << sizeof(C5) << endl;
    cout << endl;
    cout << sizeof(B53) << endl;
    cout << sizeof(B54) << endl;
    cout << sizeof(C52) << endl;
    cout << endl;
    return 0;
}
