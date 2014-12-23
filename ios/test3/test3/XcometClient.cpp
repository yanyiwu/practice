//
//  XcometClient.cpp
//  test3
//
//  Created by yanyiwu on 14/12/22.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#include "XcometClient.h"
#include <iostream>
#include <unistd.h>

using namespace std;

namespace Xcomet {
    XcometClient::XcometClient(const string& ip, int port)
        : socket_(ip, port)
    {
        cout << __FILE__ << __LINE__ << "init" << endl;
    }
    XcometClient::~XcometClient()
    {
        cout << __FILE__ << __LINE__ << "release" << endl;
    }
    XcometClient* XcometClient::instance()
    {
        cout << __FILE__ << __LINE__ << "instance";
        static XcometClient client("127.0.0.1", 3333);
        client.start(); //TODO unsafe
        return &client;
    }

    void XcometClient::run()
    {
        int ret;
        while (socket_.connect() == -1) {
            cout << "retry connecting ..." << endl;
            usleep(2000000);
        }
        

        

        const char * senddata = "POST / HTTP/1.1\r\nUser-Agent: XcometClient\r\nHost: 127.0.0.1:3333\r\nAccept: */*\r\n\r\n";
        socket_.send(senddata);
        
        string data;
        while(true)
        {
            ret = socket_.recv(data);
            cout << __FILE__ << __LINE__ << endl;
            cout << data << endl;
        }
    }

    void XcometClient::start()
    {
        cout << "XcometClient::start()" << endl;
        IThread::start();
    }
}
