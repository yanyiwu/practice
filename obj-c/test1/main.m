//
//  main.m
//  test1
//
//  Created by yanyiwu on 14/12/20.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Fraction.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Fraction *myFraction;
        
        myFraction = [[Fraction alloc] init];

        [myFraction setNumerator: 1];
        myFraction.denominator = 3;
        
        [myFraction setTo:100 over:300];

        NSLog(@"The value of myFraction is:");
        [myFraction print];
    }
    return 0;
}
