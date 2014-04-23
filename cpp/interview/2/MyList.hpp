#ifndef MYLIST_H
#define MYLIST_H

#include <iostream>
#include <cstdlib>
#include <cstdio>
using namespace std;

template <class T = size_t>
class MyListNode
{
    public:
        T value;
        MyListNode* prev;
        MyListNode* next;
        bool operator < (const MyListNode& rhs) const
        {
            return value < rhs.value;
        }
};

template <class T, class NodeType = MyListNode<T> >
class MyList
{
    public:
        typedef T value_type;
        typedef NodeType * iterator;
        typedef const NodeType* const_iterator;
    public:
        MyList()
        {
            _head = new NodeType();
            _head->next = _head;
            _head->prev = _head;
        };
        ~MyList(){clear();};
    public:
        void clear()
        {
            //TODO
        }
        bool insert(iterator iter, const value_type& value )
        {
            if(!iter)
            {
                return false;
            }
            iterator ptNode = new NodeType();
            ptNode->value = value;
            ptNode->prev = iter;
            ptNode->next = iter->next;

            iter->next = ptNode;
            ptNode->next->prev = ptNode;

            return true;
        }
        iterator erase(iterator iter)
        {
            if(!iter)
            {
                return iter;
            }
            iterator ret = iter->next;
            iter->prev->next = iter->next;
            iter->next->prev = iter->prev;
            delete iter;
            return ret;
        }
        void ordered_insert(const value_type& value)
        {
            if(empty())
            {
                insert(_head, value);
                return;
            }
            iterator iter = _head->next;
            while(iter != _head)
            {
                if(_head == iter->next || iter->next->value > value)
                {
                    insert(iter, value);
                    return;
                }
                iter = iter->next;
            }
        }
        void move_back(const T & value)
        {
            if(empty())
            {
                return;
            }
            iterator iter = _head->next;
            while(iter != end())
            {
                if(iter->value == value)
                {
                    if(iter->next == end()) // is the last element in list
                    {
                        return;
                    }
                    insert(_head->prev, value);
                    erase(iter);
                    return;
                }
                iter = iter->next;
            }
        }
        bool empty() const
        {
            return _head == _head->next;
        }

        iterator begin()
        {
            return _head->next;
        }

        iterator end()
        {
            return _head;
        }

        iterator rbegin()
        {
            return _head->prev;
        }
        iterator rend()
        {
            return _head;
        }



    private:
        iterator _head;
};

#endif
