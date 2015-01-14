#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string>
#include <iostream>
#include <assert.h>

using namespace std;

int main() {
  int sockfd;
  sockfd = socket(AF_INET, SOCK_RAW, 6);
  
  const int on = 1;
  if(setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on)) < 0) {
    cout << "setsockopt failed" << endl;
    exit(1);
  }

  
  return 0;
}
