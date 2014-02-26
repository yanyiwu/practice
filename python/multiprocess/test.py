from multiprocessing import Process

import time

def funct(arg1):
    print arg1



if __name__ == '__main__':
    work_num = 5
    procs = []
    for i in range(work_num):
        p = Process(target = funct, args = (i,))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    
