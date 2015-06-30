#include <iostream>
#include <cmath>
#include <assert.h>
#include <memory.h>
#include <stdlib.h>
#include <deque>

using namespace std;

struct SkipListNode {
  int id;
  SkipListNode* nexts[1];
};

SkipListNode* NewSkipListNode(int level, int id) {
  SkipListNode* node = (SkipListNode*)malloc(sizeof(SkipListNode) + level * sizeof(SkipListNode*));
  node->id = id;
  memset(node->nexts, 0, level * sizeof(SkipListNode*));
  return node;
}

void FreeSkipListNode(SkipListNode* node) {
  free(node);
}

class SkipList {
 public:
  SkipList(const deque<int>& dq) {
    size_t node_number = dq.size();
    assert(node_number);
    max_level_ = log2(node_number);
    assert(max_level_ > 0);
    cout << __FILE__ << __LINE__ << endl;
    cout << node_number << endl;
    cout << max_level_ << endl;
    head_ = NewSkipListNode(max_level_, 0); // TODO set header id = 0
    memset(head_->nexts, 0, max_level_ * sizeof(SkipListNode*)); // set NULL
    Build(dq);
  }
  ~SkipList() {
  }
  int Find(int id) const {
    SkipListNode* node = head_;
    SkipListNode* next_node = NULL;
    for (int i = max_level_ - 1; i >= 0; i--) {
      while ((next_node = node->nexts[i]) != NULL && id >= next_node->id) {
        if (id == next_node->id) {
          return id;
        }
        node = next_node;
      }
    }
    return 0; // NOT FOUND
  }
  void Print() const {
    cout << "===" << endl;
    for (int i = max_level_ - 1; i >= 0; i--) {
      SkipListNode* node = head_;
      cout << node->id << ",";
      while ((node = node->nexts[i]) != NULL) {
        cout << node->id << ",";
      }
      cout << endl;
    }
    cout << "===" << endl;
  }
 private:
  void Build(const deque<int>& dq) {
    for(deque<int>::const_reverse_iterator iter = dq.rbegin(); 
          iter != dq.rend(); iter++) {
      PushFront(*iter);
    }
  }
  void Destory() {
  }
  void PushFront(int id) {
    int level = RandomLevel(); //TODO
    SkipListNode* node = NewSkipListNode(level, id);
    for (int i = 0; i < level; i++) {
      node->nexts[i] = head_->nexts[i];
      head_->nexts[i] = node;
    }
  }
  int RandomLevel() const {
    int level = 1;
    while (rand() % 2 && level < max_level_) {
      level++;
    }
    return level;
  }

  int max_level_;
  SkipListNode* head_;
};

int main() {
  const size_t N = 8;
  deque<int> dq;
  for (size_t i = 1; i <= N; i++) {
    dq.push_back(i);
  }
  SkipList skiplist(dq);
  skiplist.Print();
  assert(N == skiplist.Find(N));
  assert(1 == skiplist.Find(1));
  assert(0 == skiplist.Find(0));
  assert(0 == skiplist.Find(N + 1));
  return 0;
}
