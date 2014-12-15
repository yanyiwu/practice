#ifndef FOO_HPP
#define FOO_HPP

#include <iostream>

using namespace std;

namespace foons 
{
    class Foo
    {
        public:
            Foo()
            {
            }
            ~Foo()
            {
            }
        public:
            void Hello()
            {
                cout << __FILE__ << __LINE__ << "helloworld." << endl;
            }
    };
}

#endif
