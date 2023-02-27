package com.hello;

public class ShowInt implements IShowGeneric<Integer>{

    @Override
    public void show(Integer data)
    {
        System.out.println("Show Integer: " + data);
    }
}

