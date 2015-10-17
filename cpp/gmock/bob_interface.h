#ifndef BOB_INTERFACE_H
#define BOB_INTERFACE_H

class BobInterface {
 public:
  virtual ~BobInterface() {
  }
  
  virtual int Add(int x, int y) = 0;
}; // class BobInterface

#endif // BOB_INTERFACE_H
