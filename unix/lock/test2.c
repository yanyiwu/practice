/*
 *
 * http://zhu8337797.blog.163.com/blog/static/1706175492011229112420419/
 *
 *
 * 程序一次对 5 个字节的区域进行锁定测试。如果被测试区域之前已经被别的程序锁定(共享锁，独占锁)，那么锁定测试就会失败，至于被锁定的类型可以从元素 l_type 中看出：l_type 为 0 时，是共享锁；l_ytpe 为 1 时是独占锁。
 * 其实在 /usr/include/bits/fcntl.h 文件中其实定义了这里的 0 和 1 所代表的值：
假如被测试区域没有被别的程序实施锁定操作，则返回可以对其锁定的提示信息。
l_pid 一开始被设置为 -1，这是非法值。如果被测试的区域被一个进程锁定，那么 l_pid 就会被修改为这个进程的标识符，反之就不会改变而仍然为 -1。
 */

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>

const char *test_file = "/tmp/test_lock";
#define SIZE_TO_TRY 10

void show_lock_info(struct flock *to_show);

int main() {
  int file_desc;
  int res;
  struct flock region_to_test;
  int start_byte;

  /* Open a file descriptor */
  file_desc = open(test_file, O_RDWR | O_CREAT, 0666);
  if (!file_desc) {
    fprintf(stderr, "Unable to open %s for read/write", test_file);
    exit(EXIT_FAILURE);
  }

  for (start_byte = 0; start_byte < 60; start_byte += SIZE_TO_TRY) {
    region_to_test.l_type = F_WRLCK;
    region_to_test.l_whence = SEEK_SET;
    region_to_test.l_start = start_byte;
    region_to_test.l_len = SIZE_TO_TRY;
    region_to_test.l_pid = -1;

    printf("Testing F_WRLCK on region from %d to %d\n",
           start_byte, start_byte + SIZE_TO_TRY);
    /* Now test lock on the file */
    res = fcntl(file_desc, F_GETLK, &region_to_test);
    if (res == -1) {
      fprintf(stderr, "F_GETLK failed\n");
      exit(EXIT_FAILURE);
    }
    if (region_to_test.l_pid != -1) {
      printf("Lock would fail. F_GETLK returned: ");
      show_lock_info(&region_to_test);
    } else {
      printf("F_WRLCK - Lock would succeed\n");
    }
    ///* Now repeat the test with a shared(read)lock. Set up the region you wish to test again */
    //region_to_test.l_type = F_RDLCK;
    //region_to_test.l_whence = SEEK_SET;
    //region_to_test.l_start = start_byte;
    //region_to_test.l_len = SIZE_TO_TRY;
    //region_to_test.l_pid = -1;
    //printf("Testing F_RDLCK on region from %d to %d\n", start_byte, start_byte + SIZE_TO_TRY);
    ///* Test the lock on the file again */
    //res = fcntl(file_desc, F_GETLK, &region_to_test);
    //if (res == -1) {
    //    fprintf(stderr, "F_GETLK failed\n");
    //    exit(EXIT_FAILURE);
    //}
    //if (region_to_test.l_pid != -1) {
    //    printf("Lock would fail. F_GETLK return: ");
    //    show_lock_info(&region_to_test);
    //}
    //else {
    //    printf("F_RDLCK - Lock would secceed\n");
    //}
  }
  close(file_desc);
  exit(EXIT_SUCCESS);
}
void show_lock_info(struct flock *to_show) {
  printf("\tl_type %d, ", to_show->l_type);
  printf("l_whence %d, ", to_show->l_whence);
  printf("l_start %d, ", (int)to_show->l_start);
  printf("l_len %d, ", (int)to_show->l_len);
  printf("l_pid %d\n", to_show->l_pid);
}
