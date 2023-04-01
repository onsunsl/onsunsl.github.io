import java.util.Arrays;
import java.util.List;
import java.util.function.Predicate;


/**
 * lambda & h函数式
 */
public class LambdaDemo3 {

    /**
     * 遍历list 做predicate接口操作
     *
     * @param list      带操作数列表List<Integer>
     * @param predicate 操作接口
     */
    public static void action(List<Integer> list, Predicate<Integer> predicate) {
        StringBuilder outStr = new StringBuilder();

        // 遍历
        for (Integer n : list) {

            // 运行操作
            if (predicate.test(n)) {
                outStr.append(n).append(", ");
            }
        }
        System.out.println(outStr);
    }

    public static void main(String[] args) {
        List<Integer> list = Arrays.asList(1, 2, 3, 4, 4);

        System.out.println("全部数据:");
        action(list, n -> true);

        System.out.println("偶数有:");
        action(list, n -> n % 2 == 0);


        System.out.println("奇数有:");
        action(list, n -> n % 2 == 1);

        System.out.println("大于10有:");
        action(list, n -> n > 10);

    }
}

/**
 * Java 1.8 添加的
 * java.util.function包下的函数式接口
 * <p>
 * 1	BiConsumer<T,U> 代表了一个接受两个输入参数的操作，并且不返回任何结果
 * <p>
 * 2	BiFunction<T,U,R> 代表了一个接受两个输入参数的方法，并且返回一个结果
 * <p>
 * 3	BinaryOperator<T> 代表了一个作用于于两个同类型操作符的操作，并且返回了操作符同类型的结果
 * <p>
 * 4	BiPredicate<T,U> 代表了一个两个参数的boolean值方法
 * <p>
 * 5	BooleanSupplier 代表了boolean值结果的提供方
 * <p>
 * 6	Consumer<T> 代表了接受一个输入参数并且无返回的操作
 * <p>
 * 7	DoubleBinaryOperator 代表了作用于两个double值操作符的操作，并且返回了一个double值的结果。
 * <p>
 * 8	DoubleConsumer 代表一个接受double值参数的操作，并且不返回结果。
 * <p>
 * 9	DoubleFunction<R> 代表接受一个double值参数的方法，并且返回结果
 * <p>
 * 10	DoublePredicate 代表一个拥有double值参数的boolean值方法
 * <p>
 * 11	DoubleSupplier 代表一个double值结构的提供方
 * <p>
 * 12	DoubleToIntFunction 接受一个double类型输入，返回一个int类型结果。
 * <p>
 * 13	DoubleToLongFunction 接受一个double类型输入，返回一个long类型结果
 * <p>
 * 14	DoubleUnaryOperator 接受一个参数同为类型double,返回值类型也为double 。
 * <p>
 * 15	Function<T,R> 接受一个输入参数，返回一个结果。
 * <p>
 * 16	IntBinaryOperator 接受两个参数同为类型int,返回值类型也为int 。
 * <p>
 * 17	IntConsumer 接受一个int类型的输入参数，无返回值 。
 * <p>
 * 18	IntFunction<R> 接受一个int类型输入参数，返回一个结果 。
 * <p>
 * 19	IntPredicate 接受一个int输入参数，返回一个布尔值的结果。
 * <p>
 * 20	IntSupplier 无参数，返回一个int类型结果。
 * <p>
 * 21	IntToDoubleFunction 接受一个int类型输入，返回一个double类型结果 。
 * <p>
 * 22	IntToLongFunction 接受一个int类型输入，返回一个long类型结果。
 * <p>
 * 23	IntUnaryOperator 接受一个参数同为类型int,返回值类型也为int 。
 * <p>
 * 24	LongBinaryOperator 接受两个参数同为类型long,返回值类型也为long。
 * <p>
 * 25	LongConsumer 接受一个long类型的输入参数，无返回值。
 * <p>
 * 26	LongFunction<R> 接受一个long类型输入参数，返回一个结果。
 * <p>
 * 27	LongPredicate R接受一个long输入参数，返回一个布尔值类型结果。
 * <p>
 * 28	LongSupplier 无参数，返回一个结果long类型的值。
 * <p>
 * 29	LongToDoubleFunction 接受一个long类型输入，返回一个double类型结果。
 * <p>
 * 30	LongToIntFunction 接受一个long类型输入，返回一个int类型结果。
 * <p>
 * 31	LongUnaryOperator 接受一个参数同为类型long,返回值类型也为long。
 * <p>
 * 32	ObjDoubleConsumer<T> 接受一个object类型和一个double类型的输入参数，无返回值。
 * <p>
 * 33	ObjIntConsumer<T> 接受一个object类型和一个int类型的输入参数，无返回值。
 * <p>
 * 34	ObjLongConsumer<T> 接受一个object类型和一个long类型的输入参数，无返回值。
 * <p>
 * 35	Predicate<T> 接受一个输入参数，返回一个布尔值结果。
 * <p>
 * 36	Supplier<T> 无参数，返回一个结果。
 * <p>
 * 37	ToDoubleBiFunction<T,U> 接受两个输入参数，返回一个double类型结果
 * <p>
 * 38	ToDoubleFunction<T> 接受一个输入参数，返回一个double类型结果
 * <p>
 * 39	ToIntBiFunction<T,U> 接受两个输入参数，返回一个int类型结果。
 * <p>
 * 40	ToIntFunction<T> 接受一个输入参数，返回一个int类型结果。
 * <p>
 * 41	ToLongBiFunction<T,U> 接受两个输入参数，返回一个long类型结果。
 * <p>
 * 42	ToLongFunction<T> 接受一个输入参数，返回一个long类型结果。
 * <p>
 * 43	UnaryOperator<T> 接受一个参数为类型T,返回值类型也为T。
 */