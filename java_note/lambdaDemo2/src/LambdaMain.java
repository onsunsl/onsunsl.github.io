import java.time.Instant;
import java.util.function.BinaryOperator;

/**
 * 展示函数式接口与Lambda 的配合
 * FunctionalInterface 注解实现一个函数式的接口， 有且只能有一个接口，多了会编译报错
 * 但是： default 接口个数不限制（类似C++虚函数）
 *       static  静态接口个数也不限制
 */
@FunctionalInterface
public interface LambdaMain<T> {

    // 未实现的方式类似C++的纯虚函数
    T add(T a, T b);

    // 这个方法被@FunctionalInterface 再编译时候拦截
    // void hello();

    // 已经实现的这里类似于C++ 里的虚方法，可以被子类覆盖(属于对象的)
    default void defaultMethod() {
        System.out.println("default方法的默认实现");
    }

    // 这里类似于C++ 里的静态方法， 子类
    static void staticMethod() {
        System.out.println("static方法的默认实现");
    }

    static void main(String[] args) {
        System.out.println("Java的接口也看运行");

        LambdaMain<Integer> intObj = (a, b) -> a + b;
        System.out.println(intObj.add(1, 2));

        LambdaMain<Double> floatObj = (a, b) -> a + b;
        System.out.println(floatObj.add(1.5, 22.5));

        LambdaMain<String> strObj = (a, b) -> a + b;
        System.out.println(strObj.add("hello", " world"));

        strObj.defaultMethod();
        LambdaMain.staticMethod();

    }
}


class LambdaMainSub<T> implements LambdaMain<T> {


    @Override
    public T add(T a, T b) {

        if (a instanceof Number && b instanceof Number) {
            Integer c = (Integer) a + (Integer) b;
            return (T) c;
        }

        return a;
    }

    // 这里不用@override也会覆盖父类的方法, 如果没有定义会调用父类的方法
    public void defaultMethod() {
        System.out.println("LambdaMainSub的default方法的默认实现");
    }

    static void staticMethod() {
        System.out.println("LambdaMainSub的static方法的默认实现");
    }

    public static void main(String[] args) {
        System.out.println("LambdaMainSub main");

        LambdaMain<Integer> obj = new LambdaMainSub<Integer>();
        System.out.println(obj.add(1, 2));
        obj.defaultMethod();
        LambdaMainSub.staticMethod();
    }
}


