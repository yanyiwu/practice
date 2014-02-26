#include "shingle.h"
#include <string>
#include <sstream>
#include <iostream>
#include <stdint.h>
#include <fstream>
#include <cassert>

using namespace std;

const size_t WINDOW_SIZE = 6;
const size_t N_MINIMA = 84;
const size_t N_SUPERSHINGLES = 6;


int nextChar(char ** ptr)
{
    char res = **ptr;
    if(!res)
    {
        return -1;
    }
    (*ptr)++;
    return res;
}

void ContentStrToCharacterArray(const string& strContent, char* &characterArray, int &len)
{
    int length = strContent.length();
    characterArray = new char[length*2+1];

    int lastEndPos = -1; // 最后一个句号的位置;

    int k = 0;
    for (int i=0; i<length;)
    {
        unsigned char a = (unsigned char)strContent[i];
        if (a < 0x80)
        {
            i = i + 1;
        }
        else if (a >= 0xC0 && a < 0xE0)
        {
            i = i + 2;
        }
        else if (a >= 0xE0 && a < 0xF0)
        {
            // 汉字的Unicode编码：4E00～9FA5,
            // UTF-8：E4 B8 80 ~ E9 BE A5
            unsigned char c1 = strContent[i];
            unsigned char c2 = strContent[i+1];
            unsigned char c3 = strContent[i+2];

            int nUtf8Code = 0;
            for (int j=0; j<3; j++)
            {
                nUtf8Code = nUtf8Code << 8;
                nUtf8Code += (unsigned char)strContent[i+j];
            }

            if (nUtf8Code >= 0xE4B880 && nUtf8Code <= 0xE9BEA5)
            {
                characterArray[k++] = strContent[i];
                characterArray[k++] = strContent[i+1];
                characterArray[k++] = strContent[i+2];
                characterArray[k++] = ' ';
            }

            if(nUtf8Code == 0xE38082) // 记录最后一个句号位置
            {
                lastEndPos = k;
            }
            i = i + 3;
        }
        else if (a >= 0xF0 && a < 0xF8)
        {
            i = i + 4;
        }
        else if (a >= 0xF8 && a < 0xFC)
        {
            i = i + 5;
        }
        else 
        {
            i = i + 6;
        }
    }

    if(lastEndPos != -1)
    {
        characterArray[lastEndPos] = '\0';
        len = lastEndPos;
    }
    else
    {
        characterArray[k] = '\0';
        len = k;
    }
}



int funct(char * content)
{
    uint64_t res[N_SUPERSHINGLES];
    shingle_t shingleHandle = shingle_new(WINDOW_SIZE, N_MINIMA);
    fprint_t minima[N_MINIMA];
    fprint_t supershingles[N_SUPERSHINGLES];

	int nCharacterLen = 0;
	char* characterArray = NULL;

    ContentStrToCharacterArray(content, characterArray, nCharacterLen);
    //characterArray = content;

    char* tstr = characterArray;

    shingle_stream(shingleHandle, (int(*) (void *)) nextChar, (void *)&tstr, minima);

    shingle_supershingle(shingleHandle, minima, supershingles, N_SUPERSHINGLES);
    for(size_t i = 0; i < N_SUPERSHINGLES; i++)
    {
        res[i] = supershingles[i];
        cout <<__FILE__<<__LINE__<< i << ": " << res[i] << endl;
    }
    shingle_destroy(shingleHandle);

    delete [] characterArray;

    return 0;

}

int main(int argc, char * argv[])
{
    char * content = "我是蓝翔技工拖拉机学院手扶拖拉机专业的 不用多久，我就会升职加薪，当上总经理，出任CEO，迎娶白富 美，走上人生巅峰。";
    string s;
    {
        ifstream ifs("testdata/news_content");
        assert(ifs);
        istreambuf_iterator<char> beg(ifs), end;
        s.assign(beg, end);
        //s.assign(content);
        ifs.close();
        funct((char*)s.c_str());
    }

    cout<<endl;

    {
        ifstream ifs("testdata/news_content.3");
        assert(ifs);
        istreambuf_iterator<char> beg(ifs), end;
        s.assign(beg, end);
        ifs.close();
        funct((char*)s.c_str());
    }
    return 0;
}
