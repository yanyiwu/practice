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
  var count = 0;
  var searchResults = [];
  for (var i = 0; i < words.length; i++) {
    search(words[i], function (res) {
      searchResults[count++] = res;
      if (count == words.length) {
        callback(searchResults);
      } 
    })
  }
}

var words = ["x1", "x2", "x3", "x4"];

multiSearch(words, function(responses) {
  var sum = 0;
  for (var i = 0; i < responses.length; i++) {
    sum += responses[i].length;
  }
  console.log(sum);
});
