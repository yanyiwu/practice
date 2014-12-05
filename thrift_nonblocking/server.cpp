#include <event2/event.h>
#include <event2/buffer.h>
#include <event2/bufferevent.h>
#include <event2/util.h>

#include <netinet/in.h>
/* For socket functions */
#include <sys/socket.h>
/* For fcntl */
#include <fcntl.h>

#include <assert.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

#include <iostream>

using namespace std;


enum CONN_STATUS {
  READ,
  WRITE,
  CLOSE
};

struct TConnection {
  evutil_socket_t sock;
  CONN_STATUS status;
};

const char * STR1 = "12345";
evutil_socket_t notificationPipeFDs[2];

void AcceptCB(evutil_socket_t listener, short event, void * arg) {
    struct event_base * base = (struct event_base*)arg;
    struct sockaddr_storage ss;
    socklen_t slen = sizeof(ss);
    int fd = accept(listener, (struct sockaddr*)&ss, &slen);
    if(fd < 0) {
        perror("accept");
    } else if (fd > FD_SETSIZE) {
        cout << __FILE__ << __LINE__ << endl;
        close(fd);
    } else {
        cout << __FILE__ << __LINE__ << endl;
        int size = strlen(STR1);
        TConnection conn;
        conn.sock = fd;
        int ret = send(notificationPipeFDs[1], &conn, sizeof(conn), 0);
        assert(ret == sizeof(conn));
    }
}

void notifyHandler(evutil_socket_t fd, short which, void* ctx) {
    cout << __FILE__ << __LINE__ << endl;
    TConnection conn;
    int ret = recv(notificationPipeFDs[0], &conn, sizeof(conn), 0);
    cout << conn.sock << endl;
}

int main() {
    evutil_socket_t listener;
    struct sockaddr_in sin;
    struct event_base * base;
    struct event *listener_event;
    base = event_base_new();
    sin.sin_family = AF_INET;
    sin.sin_addr.s_addr = 0;
    sin.sin_port = htons(8888);

    listener = socket(AF_INET, SOCK_STREAM, 0);
    evutil_make_socket_nonblocking(listener);

    if(bind(listener, (struct sockaddr*)&sin, sizeof(sin)) < 0) {
        perror("bind");
        return -1;
    }
    if(listen(listener, 16) < 0) {
        perror("listen");
        return -1;
    }

    listener_event = event_new(base, listener, EV_READ | EV_PERSIST, AcceptCB, base);
    event_add(listener_event, NULL);


    if(evutil_socketpair(AF_LOCAL, SOCK_STREAM, 0, notificationPipeFDs) == -1) {
        perror("aevutil_socketpair");
        return -1;
    }
    if(evutil_make_socket_nonblocking(notificationPipeFDs[0]) < 0 ||
                evutil_make_socket_nonblocking(notificationPipeFDs[1])<0  ) {
        perror("evutil_make_socket_nonblocking");
        return -1;
    }

    struct event * notification_reader = event_new(base, notificationPipeFDs[0], EV_READ|EV_PERSIST, notifyHandler, NULL);
    event_add(notification_reader, NULL);

    event_base_dispatch(base);
    return 0;
}
