var Promise = require("bluebird");

function search(word, callback) {
    console.log("searching " + word);
    callback("search result of " + word);
}

function test1() {
    var promise = new Promise(function (resolve, reject) {
        search("helloword", resolve);
    });

    promise.then(function (value) {
        console.log(value);
    });
}

function test2() {
    var promise = new Promise(function (resolve, reject) {
        search("helloword2", resolve);
    });

    promise.then(function (value) {
        return value + "then1";
    }).then(function (value) {
        console.log(value);
    });
}

function test3() {
    var words = ["x1", "x2", "x3"];
    var promises = [];
    for (var i = 0; i < words.length; i++ ) {
        promises.push(new Promise(function (resolve) {
            search(words[i], resolve);
        }));
    }
    Promise.all(promises).then(function (values) {
        console.log(values);
    });
}

test3();
