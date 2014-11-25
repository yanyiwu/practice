/* For sockaddr_in */
#include <netinet/in.h>
/* For socket functions */
#include <sys/socket.h>
/* For fcntl */
#include <fcntl.h>

#include <event2/event.h>
#include <event2/buffer.h>
#include <event2/bufferevent.h>

#include <assert.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

    struct event *ev;
    struct event* ev2;
struct event_base *base;

static void cb2(int sock, short which, void* arg) {
    printf("cb2 %s %d\n", __FILE__ , __LINE__);
}

static void cb(int sock, short which, void *arg) {
    /* Whoops: Calling event_active on the same event unconditionally
       from within its callback means that no other events might not get
       run! */

    switch(which) {
        case EV_WRITE:
            //printf("%s %d\n", __FILE__ , __LINE__);
            break;
        case EV_READ:
            //printf("%s %d\n", __FILE__ , __LINE__);
            break;
        default:
            //printf("%s %d\n", __FILE__ , __LINE__);
            break;
    }
    printf("%s %d\n", __FILE__ , __LINE__);
    event_active(ev, EV_WRITE, 0);
    //event_active(ev2, 0, 0);
}


struct Arg {
    int i1;
    int i2;
};

int main(int argc, char **argv) {
    base = event_base_new();
    //ev = event_new(base, -1, EV_PERSIST|EV_READ, cb, NULL);
    ev = event_new(base, -1, EV_PERSIST|EV_READ, cb, NULL);
    ev2= event_new(base, -1, EV_PERSIST|EV_READ, cb2, NULL);
    event_add(ev, NULL);
    event_add(ev2, NULL);
    //event_active(ev, EV_WRITE, 0);
    event_active(ev, 0, 0);
    event_base_dispatch(base);
    return 0;
}
