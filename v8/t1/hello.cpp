#include <v8.h>

using namespace v8;

int main(int argc, char* argv[])
{
    // Get the default Isolate created at startup
    //Isolate* isolate = Isolate::GetCurrent();
    
    // create a stack-allocated handle scope;
    HandleScope handle_scope;
    
    // create a new context;
    Handle<Context> context = Context::New();// = Context::New(isolate);
    
    // Enter the context for compiling and running the hello world script.
    Context::Scope context_scope(context);
    
    // create a string containing the JavaScript source code.
    Handle<String> source = String::New("'Hello' + ', World!'");
    
    // Compile the source code.
    Handle<Script> script = Script::Compile(source);
    
    // Run the script to get the result.
    Handle<Value> result = script->Run();

    // Convert the result to an Utf8 string and print it.
    
    
    String::Utf8Value utf8(result);
    printf("%s\n", *utf8);
    
    return 0;
}
