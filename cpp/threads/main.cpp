#include "ThreadManager.hpp"
using namespace std;

struct SPara
{
    SOCKET hSock;
    IRequestHandler * pHandler;
    pthread_mutex_t * ppmAccept;
    bool * pShutdown;
};


void * ThreadFunct(void * param)
{
}

int main()
{
    ThreadManager
    return 0;
}
