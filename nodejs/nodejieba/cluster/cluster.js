var http = require('http');
var cluster = require('cluster');
var nodejieba = require('nodejieba');
var os = require('os');
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

if (cluster.isMaster) {
  for (var i = 0; i < os.cpus().length; i ++) {
    cluster.fork();
  }
  console.log("master started. worker number:", os.cpus().length);
}
else {
  app();
}

