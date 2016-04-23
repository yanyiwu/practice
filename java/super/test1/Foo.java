public class Foo extends Bar {
    public Foo() {
    }
    public Foo(int k) {
        super(k);
    }
    public static void main(String []args) {
        Foo foo = new Foo();
        System.out.println(foo.k);
        Foo foo2 = new Foo(3);
        System.out.println(foo2.k);
    }
}

class Bar {
    public int k = 1;
    public Bar() {
        k = 2;
    }
    public Bar(int i) {
        k = i;
    }
}
