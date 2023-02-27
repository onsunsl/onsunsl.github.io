package com.hello;

public class GenericClass<T> {
    private T data;

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    public void show()
    {
        System.out.println("Show generic class data:" + data);
    }
}
