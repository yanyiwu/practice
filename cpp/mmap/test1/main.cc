#include <iostream>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

using namespace std;

void* _map(const char *path, size_t size) {
    int fd = open(path, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
    if (fd < 0) {
        printf("shm open failed, %m\n");
        return NULL;
    }
    int ret = ftruncate(fd, size);
    if (ret < 0) {
        close(fd);
        return NULL;
    }
    void *ptr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        close(fd);
        return NULL;
    }
    return ptr;
}

#define SIZE 1024 *1024

struct BigData {
  int x;
  int y;
  int array[SIZE];
};

int main() {
  //const char* filepath = "./mmap.file";
  const char* filepath = "/dev/shm/test1";
  BigData* p = (BigData*)_map(filepath, sizeof(BigData));
  cout << p->x << endl;
  cout << p->y << endl;
  cout << sizeof(BigData) << endl;
  getchar();
  p->x = 3;
  p->y = 4;
  p->array[SIZE - 1] = 5;
  time_t start_ts = time(NULL);
  for (size_t i = 0; i < SIZE; i++) {
    p->array[i] = i;
    //cout << p->array[i] << endl;
  }
  time_t start_ts = time(NULL);
  cout << p->array[SIZE] << endl;

  getchar();
  munmap(p, sizeof(BigData));
  return 0;
}
