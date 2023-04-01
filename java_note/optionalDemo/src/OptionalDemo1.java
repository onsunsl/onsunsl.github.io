import java.util.Optional;

/**
 * Optional 判空处理
 * 1.Optional 是一个对象容器
 * 2.调用他的美一个接口会返回一个新的Optional对象
 * 3.调用不当会导致内存增长（一直new Optional）
 *
 * 它是Functional函数式变成的典型案例， 传导式或者响应式的， 每一步都依赖上一步的结果
 *
 */


// 用户实体
class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

}



public class OptionalDemo1 {

    // 普通判空处理
    String GetName1(User user) {
        if (null != user && user.getName() != null) {
            return user.getName();
        }
        return "Unknown";
    }


    // Optional 判空处理
    String GetName2(User user) {
        return Optional.ofNullable(user).map(User::getName).orElse("Unknown");
    }

    public static void main(String[] args) {
        OptionalDemo1 main = new OptionalDemo1();
        System.out.println(main.GetName1(null));
        System.out.println(main.GetName2(null));
        User u = new User("GL", 23);
        System.out.println(main.GetName1(u));
        System.out.println(main.GetName2(u));

    }
}
