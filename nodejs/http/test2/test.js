var http = require('http');

var words = ["x1", "x2", "x3", "x4"];

function search(words, callback) {
  var count = 0;
  var searchResults = [];
  for (var i = 0; i < words.length; i++) {
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
        searchResults[count++] = str;
        //console.log(count);
        //console.log(str.length);
        if (count == words.length) {
            callback(searchResults);
        }
      });
    }).end();
  }
}

search(words, function(responses) {
  var sum = 0;
  for (var i = 0; i < responses.length; i++) {
    sum += responses[i].length;
  }
  console.log(sum);
});
