#include "tinyxml2.h"
#include <iostream>

using namespace std;
using namespace tinyxml2;

int main()
{
    XMLDocument doc;
    doc.LoadFile( "city.xml" );
    const char* title = doc.FirstChildElement( "CityDetails" )->FirstChildElement( "CityDetail" )->FirstChildElement( "CityCode")->GetText();
    //cout << title << endl;
    return 0;
}
