/**
 * lambda 的基本用法
 * 可以lambda 函数赋给一个接口，然后再调用接口的方法
 */


// 一个数学操作接口（用于lambda赋值）
interface MathApi {
    int operation(int a, int b);
}


// 打印接口 （用于lambda赋值）
interface PrintApi {
    void sayMessage(String message);
}

// 打印接口2 （用于lambda赋值可变参数）
interface Outer {
    void out(String msg, String... args);
}


public class Main {

    // 一个加法
    static public int add(int a, int b) {
        return a + b;
    }

    // 根据接口操作数数值
    static public int operate(int a, int b, MathApi api) {
        return api.operation(a, b);
    }

    public static void main(String args[]) {

        // 接口可以取类的方法
        MathApi add = Main::add;

        // lambda类型声明
        MathApi addition = (int a, int b) -> a + b;

        // lambda不用类型声明
        MathApi subtraction = (a, b) -> a - b;

        // lambda大括号中的返回语句
        MathApi multiplication = (int a, int b) -> {
            return a * b;
        };

        // lambda没有大括号及返回语句
        MathApi division = (int a, int b) -> a / b;

        System.out.println("10 + 5 = " + Main.operate(10, 5, addition));
        System.out.println("10 - 5 = " + Main.operate(10, 5, subtraction));
        System.out.println("10 x 5 = " + Main.operate(10, 5, multiplication));
        System.out.println("10 / 5 = " + Main.operate(10, 5, division));
        System.out.println("10 + 5 = " + Main.operate(10, 5, add));

        // lambda参数不用括号
        PrintApi p1 = message -> System.out.println("你好 " + message);
        p1.sayMessage("Lin");

        // lambda参数用括号
        PrintApi p2 = (message) -> System.out.println("你好 " + message);
        p2.sayMessage("Liang");

        // lambda可变参数需要括号
        Outer o1 = (msg1, msg2) -> System.out.println("你好 " + msg1 + msg2[0]);
        o1.out("msg1", "msg2", "msg3");

        String a = "我是局部变量值";
        int b = 123;

        // lambda可变参数需要括号，可变参数遍历
        Outer o2 = (msg1, msg2) -> {
            System.out.println("lambda读取局部变量：" + a + b);
            for (String msg : msg2) {
                System.out.println("hello " + msg1 + " " + msg);
            }
        };
        o2.out("参数", "可变参数1", "可变参数2", "可变参数3");

    }
}
