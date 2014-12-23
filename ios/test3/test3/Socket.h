#ifndef XCOMET_SOCKET_H
#define XCOMET_SOCKET_H

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


namespace Xcomet {

using namespace std;

class Socket 
{
    public:
        static const size_t BUFFER_INIT_SIZE = 512;

        Socket(const string& ip, int port): ip_(ip), port_(port), sock_(-1)
        {
            if ((sock_ = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
                perror("socket error!");
                exit(1);
            }
        }
        ~Socket()
        {
            if(sock_ > 0) {
                ::close(sock_);
            }
        }

        int connect()
        {
            struct sockaddr_in addr;
            bzero(&addr, sizeof(addr));
            addr.sin_family = AF_INET;
            addr.sin_port = htons(port_);
            addr.sin_addr.s_addr = inet_addr(ip_.c_str());

            return ::connect(sock_, (struct sockaddr *) &addr, sizeof(struct sockaddr));
        }

        int recv(string& buffer)
        {
            assert(sock_ > 0);
            buffer.resize(BUFFER_INIT_SIZE);
            return ::recv(sock_, (char *)buffer.c_str(), buffer.size(), 0);
        }
        int send(const string& buffer)
        {
            return ::send(sock_, buffer.c_str(), buffer.size(), 0);
        }
        
    private:
        string ip_;
        int port_;

        int sock_;
};

} // namespace xcomet


#endif
