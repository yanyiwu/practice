#include <iostream>
#include <map>
#include <tr1/unordered_map>
#include <vector>
#include <stdio.h>
#include <string.h>

using namespace std;

int main()
{
    vector<int>  mp;
    mp.resize(100000000);
    for(size_t i = 0; i < 100000000; i++)
    {
        mp[i] = i;
    }
    getchar();
    return 0;
}
