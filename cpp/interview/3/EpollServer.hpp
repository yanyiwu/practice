#ifndef HUSKY_EPOLLSERVER_H 
#define HUSKY_EPOLLSERVER_H 

#include <stdio.h>
#include <string.h>

#include <cassert>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <vector>
#include <sys/epoll.h>
#include <fcntl.h>
#include "Limonp/logger.hpp"
#include "Limonp/str_functs.hpp"
#include "Limonp/std_outbound.hpp"
#include "Limonp/InitOnOff.hpp"

namespace Husky
{
    using namespace Limonp;

    const char * const TIPS_NICKNAME = "please input your nickname.";
    const char * const TIPS_NICKNAME_AGAIN = "nickname already exists. please input another nickname";
    const char * const TIPS_WELCOME_FORMAT = "welcome! current online user number is %u";

    const struct linger LNG = {1, 1};
    const struct timeval SOCKET_TIMEOUT = {5, 0};

    class EpollServer: public InitOnOff
    {
        private:
            static const size_t LISTEN_QUEUE_LEN = 1024;
            static const size_t RECV_BUFFER_SIZE = 1024*4;
            static const int MAXEPOLLSIZE = 512;
            typedef int SockFdType;
        private:
            int _host_socket;
            int _epoll_fd;
            bool _isShutDown;
            int _epollSize;
        private:
            unordered_set<string> _nicknameSet;
            unordered_map<SockFdType, string> _sockNameMap;
            unordered_map<SockFdType, string> _sockContentMap;
        public:
            explicit EpollServer(size_t port): _host_socket(-1), _isShutDown(false), _epollSize(0)
        {
            _setInitFlag(_init_epoll(port));
        };
            ~EpollServer(){};// unfinished;
        public:
            bool start()
            {
                //int clientSock;
                sockaddr_in clientaddr;
                socklen_t nSize = sizeof(clientaddr);
                struct epoll_event events[MAXEPOLLSIZE];
                int nfds, clientSock;

                while(true)
                {
                    if(-1 == (nfds = epoll_wait(_epoll_fd, events, _epollSize, -1)))
                    {
                        LogFatal(strerror(errno));
                        return false;
                    }

                    for(int i = 0; i < nfds; i++)
                    {
                        if(events[i].data.fd == _host_socket) /*new connect coming.*/
                        {
                            if(-1 == (clientSock = accept(_host_socket, (struct sockaddr*) &clientaddr, &nSize)))
                            {
                                LogError(strerror(errno));
                                continue;
                            }
                            if(!_epoll_add(clientSock, EPOLLIN | EPOLLET))
                            {
                                LogError("_epoll_add(%d, EPOLLIN | EPOLLET)", clientSock);
                                _closesocket(clientSock);
                                continue;
                            }

                            if(!_send(clientSock, TIPS_NICKNAME))
                            {
                                LogError("send failed.");
                                continue;
                            }

                        }
                        else /*client socket data to be received*/
                        {
                            SockFdType sockfd = events[i].data.fd;
                            if(!isIn(_sockNameMap, sockfd)) // new client socket
                            {
                                string nickname;
                                _receive(sockfd, nickname);
                                if(isIn(_nicknameSet, nickname) && !_send(sockfd, TIPS_NICKNAME_AGAIN))
                                {
                                    LogError("send failed.");
                                    continue;
                                }
                                _sockNameMap[sockfd] = nickname;
                                if(!_send(sockfd, string_format(TIPS_WELCOME_FORMAT, _epollSize - 1)))
                                {
                                    LogError("send welcome failed.");
                                    continue;
                                }
                            }
                            else
                            {
                                string content;
                                _receive(sockfd, content);
                                for(unordered_map<SockFdType, string>::const_iterator iter = _sockNameMap.begin(); iter != _sockNameMap.end(); iter++)
                                {
                                    SockFdType fd = iter->first;
                                    if(fd != sockfd && !_send(fd, content))
                                    {
                                        LogError("send failed.");
                                        continue;
                                    }
                                }
                            }
                            
                        }
                    }

                }
                return true;
            }
        private:
            bool _send(SockFdType sockfd, const string& content)
            {
                if(-1 == send(sockfd, content.c_str(), content.size(), 0))
                {
                    _closesocket(sockfd);
                    return false;
                }
                return true;
            }
            bool _receive(int sockfd, string& strRec)
            {
                if(!_setsockopt(sockfd))
                {
                    return false;
                }
                char recvBuf[RECV_BUFFER_SIZE];
                int nRetCode = -1;
                while(true)
                {
                    memset(recvBuf, 0, sizeof(recvBuf));
                    nRetCode = recv(sockfd, recvBuf, sizeof(recvBuf) - 1, 0);
                    if(-1 == nRetCode)
                    {
                        LogDebug(strerror(errno));
                        return false;
                    }
                    if(0 == nRetCode)
                    {
                        LogDebug("client socket orderly shut down");
                        return false;
                    }
                    strRec += recvBuf;
                    if(nRetCode != sizeof(recvBuf) - 1)
                    {
                        break;
                    }
                }

                return true;
            }
        private:
            bool _epoll_add(int sockfd, uint32_t events)
            {
                if (!_setNonBLock(sockfd)) 
                {
                    LogError(strerror(errno));
                    return false;
                }
                struct epoll_event ev;
                ev.data.fd = sockfd;
                ev.events = events;
                if(epoll_ctl(_epoll_fd, EPOLL_CTL_ADD, sockfd, &ev) < 0)
                {
                    LogError("insert socket '%d' into epoll failed: %s", sockfd, strerror(errno));
                    return false;
                }
                _epollSize ++;
                return true;
            }
            bool _init_epoll(size_t port)
            { 
                _host_socket = socket(AF_INET, SOCK_STREAM, 0);
                if(-1 == _host_socket)
                {
                    LogError(strerror(errno));
                    return false;
                }

                int nRet = 1;
                if(-1 == setsockopt(_host_socket, SOL_SOCKET, SO_REUSEADDR, (char*)&nRet, sizeof(nRet)))
                {
                    LogError(strerror(errno));
                    return false;
                }

                struct sockaddr_in addrSock;
                addrSock.sin_family = AF_INET;
                addrSock.sin_port = htons(port);
                addrSock.sin_addr.s_addr = htonl(INADDR_ANY);
                if(-1 == ::bind(_host_socket, (sockaddr*)&addrSock, sizeof(sockaddr)))
                {
                    LogError(strerror(errno));
                    _closesocket(_host_socket);
                    return false;
                }
                if(-1 == listen(_host_socket, LISTEN_QUEUE_LEN))
                {
                    LogError(strerror(errno));
                    return false;
                }

                if(-1 == (_epoll_fd = epoll_create(MAXEPOLLSIZE)))
                {
                    LogError(strerror(errno));
                    return false;
                }
                if(!_epoll_add(_host_socket, EPOLLIN))
                {
                    LogError("_epoll_add(%d, EPOLLIN) failed.", _host_socket);
                    return false;
                }
                LogInfo("create socket listening port[%u], epoll{size:%d} init ok", port, MAXEPOLLSIZE);
                return true;
            }
            void _closesocket(int sockfd)
            {
                if(-1 == close(sockfd))
                {
                    LogError(strerror(errno));
                    return;
                }
                unordered_map<SockFdType, string>::iterator iter = _sockNameMap.find(sockfd);
                if(iter != _sockNameMap.end())
                {
                    _sockNameMap.erase(iter);
                }
                _epollSize--;
            }
            bool _setsockopt(int sockfd)
            {
                if(-1 == setsockopt(sockfd, SOL_SOCKET, SO_LINGER, (const char*)&LNG, sizeof(LNG)))
                {
                    LogError(strerror(errno));
                    return false;
                }
                if(-1 == setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&SOCKET_TIMEOUT, sizeof(SOCKET_TIMEOUT)))
                {
                    LogError(strerror(errno));
                    return false;
                }
                if(-1 == setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, (const char*)&SOCKET_TIMEOUT, sizeof(SOCKET_TIMEOUT)))
                {
                    LogError(strerror(errno));
                    return false;
                }
                return true;
            }
            static bool _setNonBLock(int sockfd)
            {
                return -1 != fcntl(sockfd, F_SETFL, fcntl(sockfd, F_GETFD, 0)|O_NONBLOCK);
            }
    };
}
#endif
