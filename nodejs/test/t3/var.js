var a = 10;  
function test() {  
  a = 100;  
  console.log(a);  
  console.log(this.a);  
  var a;  
  console.log(a);  
}  

test();
new test();
