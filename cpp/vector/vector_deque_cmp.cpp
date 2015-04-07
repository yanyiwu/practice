#include <iostream>
#include <vector>
#include <deque>
#include <stdlib.h>
#include <stdio.h>

using namespace std;


void func1() {
    const size_t MAX_SIZE = 300000000;
    vector<int> vec;
    deque<int> deq;
    vec.reserve(MAX_SIZE);
    for (size_t i = 0; i < MAX_SIZE; i++) {
        vec.push_back(i);
        deq.push_back(i);
    }
    cout << vec.size() << endl;
    cout << deq.size() << endl;
    cout << vec[MAX_SIZE/2] << endl;
    cout << deq[MAX_SIZE/2] << endl;
    getchar();
}

void func2() {
    const size_t MAX_SIZE = 3000000;
    deque<deque<int> >  t1;
    deque<vector<int> > t2;
    for (size_t i = 0; i < MAX_SIZE; i++) {
        t1.push_back(deque<int>());
        //t2.push_back(vector<int>());
    }
    cout << t1.size() << endl;
    cout << t2.size() << endl;
    getchar();
}

int main() {
    func2();
    return 0;
}
