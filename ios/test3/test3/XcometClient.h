//
//  XcometClient.h
//  test3
//
//  Created by yanyiwu on 14/12/22.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#ifndef __test3__XcometClient__
#define __test3__XcometClient__

#include <stdio.h>

namespace Xcomet {
class XcometClient {
public:
    XcometClient();
    ~XcometClient();
public:
    static XcometClient* instance();
    void start();
    void stop();
};
    
} // namespace Xcomet

#endif /* defined(__test3__XcometClient__) */
