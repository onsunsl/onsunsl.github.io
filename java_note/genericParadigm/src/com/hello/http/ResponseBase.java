package com.hello.http;

/**
 * http响应基类
 */
public class ResponseBase<D> {

    /**
     * 响应消息
     */
    private String msg;

    /**
     * 响应code
     */
    private int code;

    /**
     * 响应数据
     */
    private D data;

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public D getData() {
        return data;
    }

    public void setData(D data) {
        this.data = data;
    }
}
