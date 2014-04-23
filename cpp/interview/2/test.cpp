#include "MyList.hpp"

int main()
{
    MyList<size_t> list_;
    list_.ordered_insert(0);
    list_.ordered_insert(2);
    list_.ordered_insert(1);
    for(MyList<size_t>::iterator iter = list_.begin(); iter != list_.end(); iter = iter->next)
    {
        cout<< iter->value << endl;
    }
    for(MyList<size_t>::iterator iter = list_.rbegin(); iter != list_.rend(); iter = iter->prev)
    {
        cout<< iter->value << endl;
    }
    for(size_t i = 0; i <3 ; i ++)
    {
        size_t v = rand() % 3;
        list_.move_back(v);
        printf("move back(%u)\n", v);
    }
    for(MyList<size_t>::iterator iter = list_.begin(); iter != list_.end(); iter = iter->next)
    {
        cout<< iter->value << endl;
    }
    return 0;
}
