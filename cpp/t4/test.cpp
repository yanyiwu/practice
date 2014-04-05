#include <iostream>
#include <vector>
#include <map>
using namespace std;

struct Item
{
    size_t size;
    double point;
};

void funct1()
{
    vector<Item> vec;
    map<size_t, const Item *> mp;
    size_t count = 102400;

    Item item;
    for(size_t i = 0 ; i < count; i ++)
    {
        item.size = i;
        item.point = i * 100.0;
        vec.push_back(item);
        mp[item.size] = & vec.back();
    }

    // 此处会有coredump
    for(size_t i = 0; i < count; i++)
    {
        cout<< mp[i]->size << endl;
    }
}

void funct2()
{
    vector<Item> vec;
    map<size_t, const Item *> mp;
    size_t count = 102400;

    Item item;
    for(size_t i = 0 ; i < count; i ++)
    {
        item.size = i;
        item.point = i * 100.0;
        vec.push_back(item);
    }

    for(size_t i = 0 ; i < count; i++)
    {
        mp[vec[i].size] = &vec[i];
    }

    // 此处会有coredump
    for(size_t i = 0; i < count; i++)
    {
        cout<< mp[i]->size << endl;
    }
}

int main()
{
    funct1();//coredump
    funct2();//ok
    return 0;
}
