#include <list>
#include <fstream>
#include <iostream>
#include <boost/regex.hpp>

//boost::regex e("<\\s*A\\s+[^>]*href\\s*=\\s*\"([^\"]*)\"",
//               boost::regbase::normal | boost::regbase::icase);
boost::regex e("([\\w ]+)",
               boost::regbase::normal | boost::regbase::icase);

//void load_file(std::string& s, std::istream& is)
//{
//   s.erase();
//   //
//   // attempt to grow string buffer to match file size,
//   // this doesn't always work...
//   s.reserve(is.rdbuf()-&gtin_avail());
//   char c;
//   while(is.get(c))
//   {
//      // use logarithmic growth stategy, in case
//      // in_avail (above) returned zero:
//      if(s.capacity() == s.size())
//         s.reserve(s.capacity() * 3);
//      s.append(1, c);
//   }
//}

int main(int argc, char** argv)
{
   std::string s = "hello world";
   std::list<std::string> l;

   boost::regex_split(std::back_inserter(l), s, e);
   while(l.size())
   {
     s = *(l.begin());
     l.pop_front();
     std::cout << s << std::endl;
   }
   return 0;
}
