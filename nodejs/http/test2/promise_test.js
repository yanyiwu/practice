var Promise = require("bluebird")
var http = require('http');

function search(word, callback) {
  var options = {
    host: 'www.baidu.com',
    path: '/?wd=x'
  };
  http.request(options, function(response) {
    var str = '';

    //another chunk of data has been recieved, so append it to `str`
    response.on('data', function (chunk) {
      str += chunk;
    });

    //the whole response has been recieved, so we just print it out here
    response.on('end', function () {
      //console.log(count);
      //console.log(str.length);
      callback(str);
    });
  }).end();
}

function multiSearch(words, callback) {
  var ps = [];
  for (var i = 0; i < words.length; i++) {
    var p = new Promise(function(resolve, reject) {
      search(words[i], resolve);
    });
    ps.push(p);
  }
  Promise.all(ps).then(function(values) {
    callback(values);
  });
}

var words = ["x1", "x2", "x3", "x4"];

multiSearch(words, function(responses) {
  var sum = 0;
  for (var i = 0; i < responses.length; i++) {
    sum += responses[i].length;
  }
  console.log(sum);
});
