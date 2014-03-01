#include <iostream>
#include <fstream>
#include <cstring>
#include <stdint.h>
using namespace std;
const size_t FEAT_WORD_SIZE = 16;
const size_t FEAT_SENTENCE_SIZE = 128;
struct Data
{
    char word[FEAT_WORD_SIZE];
    uint16_t count;
    char sentence[FEAT_SENTENCE_SIZE];
};
ostream & operator << (ostream & os, const Data& data)
{
    return os << data.word << data.count << data.sentence;
}
const char * DATA_FILE = "data";
void write()
{
    
    Data data;
    strcpy(data.word, "世界");
    data.count = 1;
    strcpy(data.sentence, "你好世界");
    FILE * file = fopen(DATA_FILE, "w");
    fwrite(&data, sizeof(data), 1, file);
    fclose(file);
}
void read()
{
    Data data;
    FILE * file = fopen(DATA_FILE, "r");
    fread(&data, sizeof(data), 1, file);
    cout<< data << endl;
    fclose(file);
}
int main()
{
    write();
    read();
    return 0;
}
