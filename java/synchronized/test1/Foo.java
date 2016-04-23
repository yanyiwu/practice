//package test1;

public class Foo implements Runnable {
    @Override
    public synchronized void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(Thread.currentThread().getName() + " loop " + i);
            try {
                Thread.sleep(1000);
            } catch(InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    
    public static void main(String[] args) {
        Foo foo = new Foo();
        Thread t1 = new Thread(foo, "A");
        Thread t2 = new Thread(foo, "B");
        t1.start();
        t2.start();
    }
}

