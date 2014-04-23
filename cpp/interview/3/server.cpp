#include <unistd.h>
#include <algorithm>
#include <string>
#include <ctype.h>
#include <string.h>
#include "EpollServer.hpp"

using namespace Husky;

int main(int argc, char* argv[])
{
    if(argc < 2)
    {
        printf("usage: %s <port>\n", argv[0]);
        return EXIT_FAILURE;
    }

    EpollServer sf(atoi(argv[1]));
    sf.start();
    return EXIT_SUCCESS;
}

