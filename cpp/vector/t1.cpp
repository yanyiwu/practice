#include <iostream>
#include <vector>
#include <memory.h>
#include <malloc.h>
using namespace std;

struct Node
{
    char * str;
    Node()
    {
        cout << __FILE__ << __LINE__ << endl;
        //str = new char[12];
        str = (char*)malloc(12);
    }
    Node(const Node& node)
    {
        cout << __FILE__ << __LINE__ << endl;
    }
    ~Node()
    {
        cout << __FILE__ << __LINE__ << endl;
        free(str);
    };
};

int main()
{
    vector<Node> vec;
    vec.resize(1);
    cout << vec.capacity() << endl;
    //cout << vec[1].str << endl;
    //cout << size_t(vec[1].str) << endl;
    //vec[1].str[1] = 'a';
    //cout << vec[2].str << endl;
    //cout << size_t(vec[2].str) << endl;
    //vector <int> vec2(5);
    //cout << vec2[2] << endl;
    return 0;
}
