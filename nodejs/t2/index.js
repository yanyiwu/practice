var server = require("./server");
var route = require("./route");
var requestHandlers = require("./requestHandlers");

var handle = {
    "/": requestHandlers.start,
    "/start": requestHandlers.start,
    "/upload": requestHandlers.upload,
}

server.start(route.route, handle, 8888);
