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
        ret = socket_.connect(); // TODO 
        if(ret == -1) 
        {
            cout << __FILE__ << __LINE__ << endl;
            // retry  TODO
        }

        string data;

        const char * senddata = "POST / HTTP/1.1\r\nUser-Agent: XcometClient\r\nHost: 127.0.0.1:3333\r\nAccept: */*\r\n\r\n";
        while(true)
        {
            socket_.recv(data);
            cout << __FILE__ << __LINE__ << endl;
            cout << data << endl;
            socket_.send(senddata);
        }
    }

    void XcometClient::start()
    {
        cout << "XcometClient::start()" << endl;
        IThread::start();
    }
}
