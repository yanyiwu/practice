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

#define SERVPORT 3333
#define MAXDATASIZE 100
#define SERVER_IP "127.0.0.1"
#define DATA  "this is a client message"

typedef struct MyMessage{
    int ID;
    char info[256];
}MyMessage,*pMyMessage;

int main(int argc, char* argv[]) {
    int sockfd, recvbytes;
    //char buf[MAXDATASIZE];
    MyMessage recvData;
    struct sockaddr_in serv_addr;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket error!");
        exit(1);
    }
    bzero(&serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(SERVPORT);
    serv_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(struct sockaddr))== -1) {
        perror("connect error!");
        exit(1);
    }
    write(sockfd, DATA, sizeof(DATA));
    memset((void *)&recvData,0,sizeof(MyMessage));
    if ((recvbytes = recv(sockfd, (void *)&recvData,sizeof(MyMessage), 0)) == -1) {
        perror("recv error!");
        exit(1);
    }
    //buf[recvbytes] = '\0';
    printf("Received:ID=%d,Info= %s",recvData.ID,recvData.info);
    close(sockfd);
    return 0;
}


