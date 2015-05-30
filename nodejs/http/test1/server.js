var http = require("http")

var PORT = 8888;

var content = "<html><body><li>hello word</li></body></html>";
//var content = "hello word";

var server = http.createServer(function(req, res) {
    console.log(req.url)
    if (req.url != "/") {
        res.writeHead(404, {
            'Server': 'YanyiwuServer',
            'Content-Type': 'text/json',
        });
        res.end('{"error":"not found"}');
    } else {
        console.log(req.url)
        res.writeHead(200, {
            'Server': 'YanyiwuServer',
            'Content-Type': 'text/html',
        });
        res.end(content);
    }
});

server.listen(PORT)

console.log("server start: ", PORT)
