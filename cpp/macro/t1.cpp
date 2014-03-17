#define CREATE_BRICK_SOURCE(NAME, TPL_BRICK, CONTEXT, NEXT_BRICK) \
typedef TPL_BRICK<TYPEOF(CONTEXT), TYPEOF(*NEXT_BRICK)> __C_##NAME; \
typedef __C_##NAME *__S_##NAME;\
__S_##NAME NAME(aligned_new(__C_##NAME, CONTEXT, NEXT_BRICK)); 

int main()
{
    CREATE_BRICK_SOURCE(name,tpl_brick,context,next_brick);
    return 0;
}
