#include <node.h>
#include <v8.h>
#include <string>
#include "include/MixSegment.hpp"

using namespace v8;

CppJieba::MixSegment segment;

Handle<Value> Method(const Arguments& args) {
    HandleScope scope;
    return scope.Close(String::New("world"));
}

Handle<Value> cut(const Arguments& agrs) {
    HandleScope scope;
    std::string s("世界你好");
    std::vector<std::string> res;
    //CppJieba::MixSegment segment("/home/wyy/Code/cppjieba/dict/jieba.dict.utf8", "/home/wyy/Code/cppjieba/dict/hmm_model.utf8");
    segment.cut(s, res);
    s << res;

    return scope.Close(String::New(s.c_str()));
}

void init(Handle<Object> exports) {
    segment.init("/home/wyy/Code/cppjieba/dict/jieba.dict.utf8", "/home/wyy/Code/cppjieba/dict/hmm_model.utf8");
    //printf(__FILE__);
    exports->Set(String::NewSymbol("hello"),
                FunctionTemplate::New(Method)->GetFunction());
    exports->Set(String::NewSymbol("cut"),
                FunctionTemplate::New(cut)->GetFunction());
}

NODE_MODULE(segment, init)
