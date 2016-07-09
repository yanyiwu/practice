from multiprocessing import  Process, Value, Condition, reduction
import time
import os

def proc1():
    while True:
        print os.getpid(), os.getppid()
        time.sleep(1)

def proc2():
    while True:
        print os.getpid(), os.getppid()
        time.sleep(1)

print os.getpid(), os.getppid()
p1 = Process(target=proc1)
p1.start()

p2 = Process(target=proc2)
p2.start()

p1.join()
p2.join()
