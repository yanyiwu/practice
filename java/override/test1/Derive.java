public class Derive extends Base {
    public Derive() {
        super();
        System.out.println("Derive constructed");
    }

    @Override
    public void foo() {
        System.out.println("foo in Derive");
    }
}
