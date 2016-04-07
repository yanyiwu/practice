package com.yanyiwu;

import java.io.IOException;  
import java.io.InputStream;  
import java.io.OutputStream;  

import com.sun.net.httpserver.*;  

public class MyHandler implements HttpHandler {  
    public void handle(HttpExchange t) throws IOException {  
        System.out.println(t.getRequestURI().toString());  
        InputStream is = t.getRequestBody();  
        byte[] temp = new byte[is.available()];  
        is.read(temp);  
        System.out.println(new String(temp));  
        String response = "<h3>Hello World!</h3>";  
        t.sendResponseHeaders(200, response.length());  
        OutputStream os = t.getResponseBody();  
        os.write(response.getBytes());  
        os.close();  
    }  
}  
