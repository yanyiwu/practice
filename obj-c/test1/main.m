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
        
        myFraction = [Fraction alloc];
        myFraction = [myFraction init];

        [myFraction setNumerator: 1];
        [myFraction setDenominator: 3];

        NSLog(@"The value of myFraction is:");
        [myFraction print];
    }
    return 0;
}
