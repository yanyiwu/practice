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

struct BigData {
  int x;
  int y;
};

int main() {
  const char* filepath = "./mmap.file";
  BigData* p = (BigData*)_map(filepath, sizeof(BigData));
  cout << p->x << endl;
  cout << p->y << endl;
  getchar();
  p->x = 3;
  p->y = 4;
  getchar();

  munmap(p, sizeof(BigData));
  return 0;
}
