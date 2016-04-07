package com.yanyiwu2;

import java.io.IOException;  
import java.io.InputStream;  
import java.io.OutputStream;  
import java.net.InetSocketAddress;  

import com.sun.net.httpserver.*;  
import com.yanyiwu.MyHandler;

public class MyHttpServer {  
    public static void main(String[] args) {  
        System.out.println("hello server2");
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
