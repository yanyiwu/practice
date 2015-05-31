var mongoose =  require('mongoose');
var Schema = mongoose.Schema;
mongoose.connect("mongodb://localhost:27017/test");

var UserSchema = new Schema({
    username : { type: String, default: '' ,trim : true, index: {unique: true} },
    password : { type: String, default: '' ,trim : true},
    email: { type: String, default: '' }
}, {collection: 'user'});

var User = mongoose.model('User', UserSchema);

var u= new User({username:"test",password:"123456",email:"123@qq.com"});

u.save(function(err){
    if(err) {
        console.log(err);
    }
});

//User.remove({ username: 'test' }, function (err) {
//    console.log(err);
//});

User.update({ username: 'test' }, { email: '456@qq.com' }, { multi: true }, function (err, numberAffected, raw) {
    if(err) {
        console.log(err);
    }
});


User.find({ username: 'test' }, function(err, docs) {
    if(err) {
        console.log(err);
    } else {
        console.log(docs.length);
    }
});

