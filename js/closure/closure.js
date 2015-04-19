var uniqueInterger = ( function() {
    var counter = 0;
    return function () { return counter++;}
}());
console.log(uniqueInterger())
console.log(uniqueInterger())


var uniqueInterger2 = ( function() {
    var counter = 0;
    return function () { return counter++;}
}());
console.log(uniqueInterger2())
console.log(uniqueInterger2())


var a = ( function() {
    var counter = 0;
    return function () { return counter++;}
});

var b1 = a();
var b2 = a();
console.log(b1());
console.log(b2());
console.log(b1());
console.log(b2());
