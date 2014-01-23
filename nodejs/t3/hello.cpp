#include <node.h>
#include <v8.h>
#include <string>

using namespace v8;

Handle<Value> Method(const Arguments& args) {
  HandleScope scope;
  return scope.Close(String::New("world"));
}

Handle<Value> cut(const Arguments& agrs) {
    HandleScope scope;
    std::string s("cut");
    return scope.Close(String::New(s.c_str()));
}

void init(Handle<Object> exports) {
  exports->Set(String::NewSymbol("hello"),
      FunctionTemplate::New(Method)->GetFunction());
  exports->Set(String::NewSymbol("cut"),
      FunctionTemplate::New(cut)->GetFunction());
}

NODE_MODULE(hello, init)
