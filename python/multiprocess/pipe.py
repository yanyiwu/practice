from multiprocessing import Process, Pipe

def f(pipe):
    pipe.send(1)
    print pipe.recv()
    pipe.close()

if __name__ == '__main__':
    parent_pipe, child_pipe = Pipe()
    p = Process(target=f, args=(child_pipe,))
    p.start()
    print parent_pipe.recv()
    parent_pipe.send(2)
    p.join()
