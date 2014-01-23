#include <node.h>
#include <v8.h>
#include "CppJieba/MixSegment.hpp"

using namespace v8;

CppJieba::MixSegment segment;

Handle<Value> cut(const Arguments& args) {
    HandleScope scope;

    v8::String::Utf8Value param1(args[0]->ToString());
    
    //std::string sentence(*param1);
    std::string wordsStr;
    
    std::vector<std::string> words;

    segment.cut(*param1, words);
    wordsStr << words;

    return scope.Close(String::New(wordsStr.c_str()));
}

void init(Handle<Object> exports) {
    segment.init("./dict/jieba.dict.utf8", "./dict/hmm_model.utf8");
    //printf(__FILE__);
    exports->Set(String::NewSymbol("cut"),
                FunctionTemplate::New(cut)->GetFunction());
}

NODE_MODULE(segment, init)
