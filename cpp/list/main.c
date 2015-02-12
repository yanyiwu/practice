#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>

struct ListNode {
    int value;
    struct ListNode* next;
};

struct ListNode * NewListNode(int value) {
    struct ListNode *node = (struct ListNode*)malloc(sizeof(struct ListNode));
    node->value = value;
    node->next = NULL;
    return node;
}

void Insert(struct ListNode* root, struct ListNode* node) {
    node->next = root->next;
    root->next = node;
}

void Print(struct ListNode* root) {
    struct ListNode* node = root;
    while(node != NULL) {
        printf("%d\n", node->value);
        node = node->next;
    }
    printf("\n");
}

void Delete(struct ListNode* root, int value) {
    struct ListNode* node = root;
    if(node == NULL) {
        return;
    }
    while(node->next != NULL) {
        struct ListNode* next = node->next;
        if(next->value == value) {
            struct ListNode * t = next;
            node->next = t->next;
            node = node->next;
            free(t);
            printf("delete %d\n", value);
        } else {
            node = node->next;
        }
    }
}

void Delete2(struct ListNode* root, int value) {
    struct ListNode** p = &root;
    while((*p) != NULL) {
        if((*p)->value == value) {
            struct ListNode* t = *p;
            (*p) = t->next;
            free(t);
        } else {
            p = &(*p)->next;
        }
    }
}

void func1() {
    struct ListNode * root = NewListNode(0);
    struct ListNode * node1 = NewListNode(1);
    Insert(root, node1);
    struct ListNode * node2 = NewListNode(2);
    Insert(root, node2);
    struct ListNode * node3 = NewListNode(3);
    Insert(root, node3);
    Print(root->next);
    Delete2(root->next, 2);
    Print(root->next);
}

int main() {
    func1();
    return 0;
}
