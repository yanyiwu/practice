from threading import local, enumerate, Thread, currentThread

local_data = local()
local_data.name = 'local_data'

class TestThread(Thread):
        def run(self):
                print currentThread()
                print local_data.__dict__
                local_data.name = self.getName()
                local_data.add_by_sub_thread = self.getName()
                print local_data.__dict__

if __name__ == '__main__':
        print currentThread()
        print local_data.__dict__
        
        t1 = TestThread()
        t1.start()
        t1.join()
        
        t2 = TestThread()
        t2.start()
        t2.join()
        
        print currentThread()
        print local_data.__dict__
