var something = {
  functA: function functA() {
    console.log("running functA");
  },
  functB: function functA() {
    console.log("running functB");
  },
};

something.functA();
// running functA
console.log("=====");

var somethingFunctA = something.functA;

something.functA = function () {
  console.log("before functA");
  somethingFunctA.apply(this, arguments);
}

something.functA();
// before functA
// running functA
console.log("=====");

var hint = "hint: hello";

function wrapWithHint(obj, funName) {
  var someFunction = obj[funName];
  obj[funName] = function() {
    console.log(hint);
    someFunction.apply(this, arguments);
  }
}

something.functB();
// running functB
console.log("=====");

wrapWithHint(something, "functB");

something.functB();
// hint: hello
// running functB
