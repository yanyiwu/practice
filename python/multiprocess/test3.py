from multiprocessing import  Process, Value, Condition, reduction
import time

import threading, os

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
    def run(self):
        while True:
            print os.getpid(), os.getppid()
            time.sleep(1)

def proc1():
    while True:
        print '1'
        time.sleep(1)

def proc2():
    while True:
        print '2'
        time.sleep(1)

th = MyThread()
th.start()

p1 = Process(target=proc1)
p1.start()

p2 = Process(target=proc2)
p2.start()

p1.join()
p2.join()
th.join()
