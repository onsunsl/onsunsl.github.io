package com.hello;

import java.util.ArrayList;

class AObject<T> {
    private T value;

    public T getValue() {
        return value;
    }

    public void setValue(T value) {
        this.value = value;
    }

}

public class Demo {


    /* 非泛型 -> 没有类型检查`安全性`差 */
    public static void noGenericNoSafe() {
        ArrayList list = new ArrayList();
        list.add("hello");
        list.add(123);
        System.out.println(list);
    }

    /* 泛型 -> 没有类型检查`安全性`好 */
    public static void withGenericSafe() {
        ArrayList<String> list = new ArrayList<>();
        list.add("hello");

        // 添加非String 类型编译出错
        // list.add(123);
    }

    /* 非泛型 -> 需要类型转换 */
    public static void noGenericConvert() {
        ArrayList list = new ArrayList();
        list.add("hello");
        list.add(123);

        String name = (String) list.get(0);
        int age = (int) list.get(0);
        System.out.println("name:" + name + " age:" + age);
    }

    /* 泛型 -> 消除类型转换 */
    public static void withGenericNoConvert() {
        ArrayList<String> list = new ArrayList<>();
        list.add("hello");

        String name = list.get(0);
        System.out.println("name:" + name);
    }


    public static void main(String[] args) {
        Demo.noGenericNoSafe();
        AObject<String> value1 = new AObject<>();
        AObject<Integer> value2 = new AObject<>();
        value1.setValue("123");
        value2.setValue(123);

        IShowGeneric<Integer> si = new ShowInt();
        si.show(123);

        IShowGeneric<String> ss = new ShowString();
        ss.show("1234");

        GenericClass<Integer> g = new GenericClass<>();
        g.setData(12342);
        g.show();

        GenericClass<String> g2 = new GenericClass<>();
        g2.setData("23423423");
        g2.show();
    }
}
