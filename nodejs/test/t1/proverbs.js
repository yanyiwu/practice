function onRequest(request, response) { 
    var pathname = url.parse(request.url).pathname; 
    console.log("Reqeust for " + pathname + " received."); 

    if (pathname === "/" || pathname === "/index" || pathname === "/proverb") { 
        getProverb(response); 
    } else if (pathname === "/add") { 

        if (request.method.toLowerCase() == 'post') { 
            var body = ''; 
            request.on('data', function(data) { 
                body += data; 
            }); 

            request.on('end', function() { 

                var POST = qs.parse(body); 
                add(POST.text, response); 

            }); 
        } else { 
            addProverb(response); 
        } 

    } else { 
        response.writeHead(404, { 
            "Content-Type" : "text/plain"
        }); 
        response.write("404 Not found"); 
        response.end(); 
    } 

}
function getProverb(response) { 
    var body = '<html>'
        + '<head>'
        + '<meta http-equiv="Content-Type" content="text/html; '
        + 'charset=UTF-8" />'
        + '</head>'
        + '<body style="font-size: 4em;line-height: 1.2; margin-top: 200;">'
        + '<blockquote>'+ proverbs[Math.floor(Math.random()* proverbs.length)]
        + '</blockquote>' + '</body>'
        + '</html>'; 

    response.writeHead(200, { 
        "Content-Type" : "text/html"
    }); 
    response.write(body); 
    response.end(); 

}
function addProverb(response) { 
    var body = '<html>'
        + '<head>'
        + '<meta http-equiv="Content-Type" content="text/html; '
        + 'charset=UTF-8" />'
        + '</head>'
        + '<body style="font-size: 4em;line-height: 1.2; margin-top: 200;">'
        + '<form action="/add" method="post">'
        + '<textarea name="text" rows="10" cols="60"></textarea><p>'
        + '<input type="submit" value="Submit"/>' + '</form>' + '</body>'
        + '</html>'; 

    response.writeHead(200, { 
        "Content-Type" : "text/html"
    }); 
    response.write(body); 
    response.end(); 

}
function add(proverb, response) { 
    proverbs.push(proverb); 

    var body = '<html>'
        + '<head>'
        + '<meta http-equiv="Content-Type" content="text/html; '
        + 'charset=UTF-8" />'
        + '</head>'
        + '<body style="font-size: 4em;line-height: 1.2; margin-top: 200;">'
        + '<blockquote>' + proverb + '</blockquote>' + '</body>'
        + '</html>'; 

    response.writeHead(200, { 
        "Content-Type" : "text/html"
    }); 
    response.write(body); 
    response.end(); 

}

var http = require("http");
var url = require("url");
var qs = require("querystring");
var proverbs = [ 
"The turtle wins the race.", 
    "God hides in the details.", 
    "There are two ways to write error-free programs; only the third one works.", 
    "Perfect practice makes perfect."
    ];
    http.createServer(onRequest).listen(8888);
    console.log("server is running...");
