//
//  XcometClient.cpp
//  test3
//
//  Created by yanyiwu on 14/12/22.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#include "XcometClient.h"
#include <iostream>
using namespace std;

namespace Xcomet {
    XcometClient::XcometClient()
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
        static XcometClient client;
        return &client;
    }
    void XcometClient::start()
    {
        cout << "XcometClient::start()" << endl;
    }
    void XcometClient::stop()
    {
        cout << "XcometClient::stop()" << endl;
    }
}