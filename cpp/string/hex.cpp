#include <iostream>
using namespace std;

int main()
{
    char num = 'z';
    std::cout << std::hex << num << std::dec << std::endl;
    printf("%.2X\n", num);
    cout.setf(ios::hex, ios::basefield);
    cout << "Hex: " << num << endl;

    cout.unsetf(ios::hex);
    cout << "Original format: " << num << endl;

    return 0;
}
