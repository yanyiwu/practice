
var http = require("http");
var url = require("url");
var util = require("./util");

function start(route, handle, listenPort) {
    function onRequest(request, response){
        var pathname = url.parse(request.url).pathname;
        console.log("Request for %s received.", pathname);
        var content = route(handle, pathname);
        //console.log(util.toString(request));
        response.writeHead(200, {"Content-Type":"text/plain"});
        response.write(content);
        response.end();
    }

    http.createServer(onRequest).listen(listenPort);

    console.log("server[%d] running...", listenPort);
}

exports.start = start
