#include "FileLock.h"

static const char* test_file = "/tmp/test_lock";


static int LockOrUnlock(int fd, bool lock) {
  errno = 0;
  struct flock f;
  memset(&f, 0, sizeof(f));
  f.l_type = (lock ? F_WRLCK : F_UNLCK);
  f.l_whence = SEEK_SET;
  f.l_start = 0;
  f.l_len = 0;        // Lock/unlock entire file
  return fcntl(fd, F_SETLK, &f);
}

static int LockOrUnlock(const char * fname, bool lock) {
  int fd = open(fname, O_RDWR | O_CREAT, 0644);
  if(fd < 0) {
    return fd;
  }
  int ret = LockOrUnlock(fd, true);
  return ret;
}

int main() {
  //LockOrUnlock(test_file, );
  FileLock fileLock;
  fileLock.Open(test_file);
  assert(fileLock.Ok());
  fileLock.Lock();
  assert(fileLock.Ok());
  getchar();
  fileLock.UnLock();
  assert(fileLock.Ok());
  getchar();
  return 0;
}
