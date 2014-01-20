
function start() {
    var http = require("http");
    var util = require("./util");
    var listenPort = 8888;
    function onRequest(request, response){
        console.log("Request received.");
        //console.log(util.toString(request));
        response.writeHead(200, {"Content-Type":"text/plain"});
        response.write("Hello World");
        response.end();
    }

    http.createServer(onRequest).listen(listenPort);

    console.log("server[%d] running...", listenPort);
}

exports.start = start
