import java.text.MessageFormat;

class SubClass {
    private String name;
    private int age;

    public SubClass(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "SubClass{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}';
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}

public class Main {

    private  String name;

    private  SubClass sub;

    public SubClass getSub() {
        return sub;
    }

    public void setSub(SubClass sub) {
        this.sub = sub;
    }


    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Main{" +
                "name='" + name + '\'' +
                ", sub=" + sub +
                '}';
    }

    public static void main(String[] args) {
        Main m = new Main();

        // 输出 main = Main{name='null', sub=null}
        // 说明对象new 出来成员变量是null
        System.out.println("main=" + m);


        //SubClass sub = m.getSub();
        // sub 取出来是null 不能直接使用
        // sub.setAge(123);


        SubClass sub1 = new SubClass("李四", 11);
        m.setSub(sub1);
        System.out.println("main=" + m);

        SubClass sub2 = m.getSub();

        System.out.println(MessageFormat.format("sub 和sub2是统一对象? {0}",sub1.equals(sub2)));
        System.out.println(MessageFormat.format("sub 和sub2是统一对象? {0}",sub1==sub2));

    }
}
