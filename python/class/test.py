class Foo:
    x = {}
    def __init__(self):
        pass

    def run(self):
        Foo.x[1] = 1
        pass


if __name__ == '__main__':
    foo = Foo()
    bar = Foo()
    print foo.x
    print bar.x
    foo.run()
    print foo.x
    print bar.x
