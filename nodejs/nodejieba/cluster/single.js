var http = require('http');
var nodejieba = require('nodejieba');
var url = require('url');

var port = 8080;

function app() {
  var server = http.createServer(function(request, response) {
    var s = url.parse(request.url, true).query.s;
    var words = nodejieba.cut(s);
    var res = JSON.stringify(words);
    console.log(res);
    response.end(res);
  });
  server.listen(port);
}

app();
