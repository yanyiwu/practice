#include <iostream> 
#include <cmath>
#include <fstream>
using namespace std;
int main()
{
    double a = log(double(1)/double(111948));
    cout << (sizeof(a)) << endl;
    FILE * file = fopen("tmp", "w");
    fwrite(&a, sizeof(a), 1, file);
    fclose(file);
    return 0;
}

