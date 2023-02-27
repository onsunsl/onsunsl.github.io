package com.hello.http;

public class UserInfoResponse {

    /**
     * 用户id
     */
    private String id;

    /**
     * 用户名
     */
    private String name;


    /**
     * 用户年龄
     */
    private int age;


    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
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
