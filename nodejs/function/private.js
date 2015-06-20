function Maker() {
  var count = 0;
  return function() {
    return {
      get: function() {
        return count;
      },
      increase: function() {
        count ++;
      },
      decrease: function() {
        count --;
      },
    };
  }()
}

var maker = Maker()

console.log(maker.get());
maker.increase();
console.log(maker.get());

var t = [];
console.log(t.length);
t.length = 10;
console.log(t.length);
t[2] = 2;
console.log(t.length);
t[3] = 3;
console.log(t.length);
