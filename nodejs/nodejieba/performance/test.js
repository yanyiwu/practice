var fs = require('fs');
var nodejieba = require('nodejieba');

var file = fs.readFileSync('weicheng.utf8', "utf8");
lines = file.split('\n')

var begin = new Date();
console.log(begin);
for (var cnt = 0; cnt < 50; cnt++) {
  for (var i = 0; i < lines.length; i++) {
    nodejieba.cut(lines[i]);
  }
}
var end = new Date();
console.log(end);
var ms = end.getTime() - begin.getTime();

console.log(ms + " ms");
