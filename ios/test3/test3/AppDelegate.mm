//
//  AppDelegate.m
//  test3
//
//  Created by yanyiwu on 14/12/22.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#import "AppDelegate.h"
#include "XcometClient.h"
#include <iostream>
#include <fstream>

using std::cout;
using std::endl;
using std::fstream;

@interface AppDelegate ()

@end

@implementation AppDelegate
{
    NSMutableData* mData;
}

/*
- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // Override point for customization after application launch.
    return YES;
}
*/

/*
- (NSString*) sendRequestSync:(NSString*)urlStr withContent:(NSString*)content
{
    printf("hello sendRequestSync\n");
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
    
    [request setURL:[NSURL URLWithString:urlStr]];
    [request setHTTPMethod:@"POST"];
    [request setValue:host forHTTPHeaderField:@"Host"];
    NSString *contentLength = [NSString stringWithFormat:@"%d", [content length]];
    NSString * response;
    return response;
}
 */


// http 请求开始
- (void)httpConnectionWithRequest {
    Xcomet::XcometClient* client = Xcomet::XcometClient::instance();
    NSLog(@"httpConnectionWithRequest");
    //NSString *URLPath = [NSString stringWithFormat:@"http://127.0.0.1:11257"];
    NSString *URLPath = [NSString stringWithFormat:@"http://192.168.2.28:9000/sub?uid=1&seq=1"];
    NSURL *URL = [NSURL URLWithString:URLPath];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:URL];
    
    request.HTTPMethod = @"GET";
    request.timeoutInterval = 60;
    
    NSURLConnection *conn = [NSURLConnection connectionWithRequest:request delegate:self];
    
    [conn start];
    //[conn cancel];
}

// 获取返回状态，包头信息
- (void)conncetion:(NSURLConnection*)theConnection didReceiveResponse:(NSURLResponse*)response
{
    NSInteger responseCode = [(NSHTTPURLResponse*)response statusCode];
    NSLog(@"response length=%lld statuscode %ld", [response expectedContentLength], responseCode);
}



// 接受数据
- (void)connection:(NSURLConnection*)theConnection didReceiveData:(NSData *)data
{
    if(mData == nil) {
        mData = [[NSMutableData alloc] initWithData:data];
    } else {
        [mData appendData:data];
    }
    NSLog(@"response connection");
}


// 连接失败，包含失败。
- (void)connection:(NSURLConnection*)theConnection didFailWithError:(NSError *)error
{
    NSLog(@"%s %d response error%@", __FILE__, __LINE__, [error localizedFailureReason]);
}



// 数据接受完毕
- (void)connectionDidFinishLoading:(NSURLConnection *)theConnection
{
    NSString* responseString = [[NSString alloc] initWithData:mData encoding:NSUTF8StringEncoding];
    NSLog(@"%s %d response body%@", __FILE__, __LINE__, responseString);
    UILabel *label = (UILabel *)[self.window viewWithTag:100 ];
    label.text = responseString;
}

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    //[self sendRequestSync:@"123"];
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    // Override point for customization after application launch.
    self.window.backgroundColor = [UIColor whiteColor];
    
    
    UILabel *la = [[UILabel alloc] initWithFrame:CGRectMake(50, 100, 50, 50)];
    la.text = @"图片读取";
    NSString *image_url = [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:@"xxb.bundle/images/test.jpg"];
    NSLog(@"%@", image_url);
    NSString *txt_url = [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:@"xxb.bundle/files/test.txt"];
    const char * a = [txt_url UTF8String];
    printf("%s %d %s\n", __FILE__, __LINE__, a);
    std::fstream fin(a);
    std::string str;
    while(std::getline(fin, str)) {
        cout << __FILE__ << __LINE__ << endl;
        cout << str << endl;
    }
    
    la.backgroundColor = [UIColor colorWithPatternImage:[UIImage imageWithContentsOfFile:image_url]];
    [self.window addSubview:la];
    
    // label 开始
    UILabel* label = [[UILabel alloc] initWithFrame:CGRectMake(90, 100, 140, 40)];
    label.text = @"标签";
    label.tag = 100;
    label.textAlignment = NSTextAlignmentCenter;
    [self.window addSubview:label];
    // label 结束
    
    // button 开始
    UIButton* button = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    button.frame = CGRectMake(90, 150, 140, 40);
    [button setTitle:@"按钮" forState:UIControlStateNormal];
    
    // 事件
    [button addTarget:self action:@selector(touchUpInside) forControlEvents:UIControlEventTouchUpInside];
    
    [self.window addSubview:button];
    // button 结束
    
    // textfield 开始
    
    UITextField *tf = [[UITextField alloc] initWithFrame:CGRectMake(60, 200, 200, 35)];
    //tf.tag = 101;
    tf.delegate = self;
    //tf.textColor = [UIColor redColor];
    tf.placeholder = @"用来提示用户";
    tf.borderStyle = UITextBorderStyleRoundedRect;
    [self.window addSubview:tf];
    
    
    [self.window makeKeyAndVisible];
    return YES;
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    // 隐藏输入键盘
    [textField resignFirstResponder];
    textField.text = @"hello return";
    textField.textColor = [UIColor redColor];
    return YES;
}

// 清除文字按钮点击事件
//- (BOOL)textfieldshouldclear: (UITextField*)textField {
//    return YES;
//}

- (void)touchUpInside
{
    [self httpConnectionWithRequest];
    std::cout << "cpp touchUpInside" << std::endl;
    printf("touchUpInside\n");
}

- (void)applicationWillResignActive:(UIApplication *)application {
    // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
    // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
}

- (void)applicationDidEnterBackground:(UIApplication *)application {
    // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
    // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
}

- (void)applicationWillEnterForeground:(UIApplication *)application {
    // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
}

- (void)applicationDidBecomeActive:(UIApplication *)application {
    // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}

- (void)applicationWillTerminate:(UIApplication *)application {
    // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
}

@end
