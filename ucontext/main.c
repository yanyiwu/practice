#include <ucontext.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define STACK_SIZE (1024*1024)

#define PRINT() {printf("%s %d %s\n", __FILE__, __LINE__, __func__);};

struct schedule {
};

static void
mainfunc() {
    PRINT();
}

int main() {
    char stack[STACK_SIZE];
    ucontext_t co_ctx;
    ucontext_t main_ctx;
    getcontext(&co_ctx);
    co_ctx.uc_stack.ss_sp = stack;
    co_ctx.uc_stack.ss_size = STACK_SIZE;
    co_ctx.uc_link = &main_ctx; 
    //co_ctx.uc_link = NULL; 
    makecontext(&co_ctx, mainfunc, 0);
    swapcontext(&main_ctx, &co_ctx);
    PRINT();
    return 0;
}
