package com.hello;

public class ShowString implements IShowGeneric<String>{

    @Override
    public void show(String data)
    {
        System.out.println("Show String:" + data);
    }
}
