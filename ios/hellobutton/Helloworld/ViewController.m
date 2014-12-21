//
//  ViewController.m
//  Helloworld
//
//  Created by yanyiwu on 14/12/21.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)showMessage
{
    UIAlertView *helloWorldAlert = [[UIAlertView alloc]
        initWithTitle:@"My Dear" message:@"I Love You" delegate:nil cancelButtonTitle:@"I Love you ,too." otherButtonTitles:nil];
    
    [helloWorldAlert show];
}

@end
