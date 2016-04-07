package com.yanyiwu;

import java.io.IOException;  
import java.net.InetSocketAddress;  

import com.sun.net.httpserver.*;  

public class MyHttpServer {  
    public static void main(String[] args) {  
        try {  
            HttpServer hs = HttpServer.create(new InetSocketAddress(7777), 0);  
            hs.createContext("/myrequest", new MyHandler());  
            hs.setExecutor(null);  
            hs.start();  
        } catch (IOException e) {  
            e.printStackTrace();  
        }  
    }  
}  

