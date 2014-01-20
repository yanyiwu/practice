function toString(obj){
    var t = "";
    for(var i in obj){
        var property = obj[i];
        t += i + " = " + property + "\n";
    }
    return t;
}


exports.toString = toString;
