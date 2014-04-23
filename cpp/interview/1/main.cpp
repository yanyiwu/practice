#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cstdio>
using namespace std;
int reverse_str(char * str_src, char * str_dst)
{
    if(!str_src || !str_dst)
    {
        return -1;
    }
    size_t len = strlen(str_src);//O(n)
    if(str_dst - str_src < len)//overlap
    {
        return -1;
    }
    for(size_t i = 0; i < len ; i++) 
    {
        str_dst[i] = str_src[len -1 - i];
    }
    return 0;
}

int main()
{
    char str_dst[8] = {0};
    const char* str_src = "abc";
    if(-1 == reverse_str((char*)str_src, str_dst))
    {
        fprintf(stderr, "failed.");
    }
    else
    {
        printf("%s\n", str_dst);
    }
    return 0;
}
