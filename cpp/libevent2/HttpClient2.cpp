#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <sys/socket.h>
#include <netinet/in.h>

#include <event2/bufferevent_ssl.h>
#include <event2/bufferevent.h>
#include <event2/buffer.h>
#include <event2/listener.h>
#include <event2/util.h>
#include <event2/http.h>

#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/rand.h>

static void
http_request_done(struct evhttp_request *req, void *ctx)
{
	char buffer[256];
	int nread;

	if (req == NULL) {
		/* If req is NULL, it means an error occurred, but
		 * sadly we are mostly left guessing what the error
		 * might have been.  We'll do our best... */
		struct bufferevent *bev = (struct bufferevent *) ctx;
		unsigned long oslerr;
		int printed_err = 0;
		int errcode = EVUTIL_SOCKET_ERROR();
		fprintf(stderr, "some request failed - no idea which one though!\n");
		/* Print out the OpenSSL error queue that libevent
		 * squirreled away for us, if any. */
#if 0
		while ((oslerr = bufferevent_get_openssl_error(bev))) {
			ERR_error_string_n(oslerr, buffer, sizeof(buffer));
			fprintf(stderr, "%s\n", buffer);
			printed_err = 1;
		}
#endif
		/* If the OpenSSL error queue was empty, maybe it was a
		 * socket error; let's try printing that. */
		if (! printed_err)
			fprintf(stderr, "socket error = %s (%d)\n",
				evutil_socket_error_to_string(errcode),
				errcode);
		return;
	}

	fprintf(stderr, "Response line: %d %s\n",
	    evhttp_request_get_response_code(req),
	    evhttp_request_get_response_code_line(req));

	while ((nread = evbuffer_remove(evhttp_request_get_input_buffer(req),
		    buffer, sizeof(buffer)))
	       > 0) {
		/* These are just arbitrary chunks of 256 bytes.
		 * They are not lines, so we can't treat them as such. */
		fwrite(buffer, nread, 1, stdout);
	}
}

class HttpClient {
 public:
  HttpClient() {
    Init();
  }
  ~HttpClient() {
	evhttp_connection_free(evhttpcon_);
	event_base_free(evbase_);
  }
 public:
  void Start() {
    event_base_dispatch(evbase_);
  }
  //void Query(const char* host, )
 private:
  void Init() {
    evbase_ = event_base_new();
    bev_ = bufferevent_socket_new(evbase_, -1, BEV_OPT_CLOSE_ON_FREE);
    const char * host = "yanyiwu.com";
    int port = 80;
    evhttpcon_ = evhttp_connection_base_bufferevent_new(evbase_, NULL, bev_, host, port);
    getchar();
    assert(evhttpcon_);
    struct evhttp_request* req = evhttp_request_new(http_request_done, bev_);
	struct evkeyvalq *output_headers;
	struct evbuffer * output_buffer;
    output_headers = evhttp_request_get_output_headers(req);
    evhttp_add_header(output_headers, "Host", host);
    evhttp_add_header(output_headers, "Connection", "close");
    char uri[256];
    uri[0] = '/';
    uri[1] = '\0';
    int r = evhttp_make_request(evhttpcon_, req, EVHTTP_REQ_GET, uri);
    getchar();
    assert(r == 0);
  }
 private:
  struct event_base * evbase_;
  struct bufferevent* bev_;
  struct evhttp_connection* evhttpcon_;
};


int
main(int argc, char **argv)
{
    HttpClient client;
    client.Start();
	return 0;
}


