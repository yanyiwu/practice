//
//  XcometClient.h
//  test3
//
//  Created by yanyiwu on 14/12/22.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#ifndef __test3__XcometClient__
#define __test3__XcometClient__

#include <string>
#include "Thread.h"
#include "Socket.h"

namespace Xcomet {

using namespace std;

class XcometClient: public IThread {
public:
    XcometClient(const string& ip, int port);
    virtual ~XcometClient();
public:
    static XcometClient* instance();
    virtual void run();
    virtual void start();
    
    Socket socket_;
};
    
} // namespace Xcomet

#endif /* defined(__test3__XcometClient__) */
