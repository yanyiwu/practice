#include <iostream>
using namespace std;

template<typename T>
class Tree {
  public:
    Tree() {
      root = new Node();
    }
    ~Tree() {
      delete root;
    }
    void someFunction() {
      //函数中想使用->访问Node类型中的数据成员
      cout << root->left << endl;
    }
  private:
    struct Node {
      T element;
      Node* left;
      Node* right;
    };
    Node* root;
};

int main() {
  Tree<int> t;
  t.someFunction();
  return 0;
}

