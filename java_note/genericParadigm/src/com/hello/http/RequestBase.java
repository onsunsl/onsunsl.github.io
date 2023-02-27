package com.hello.http;

/**
 * HTTP请求基类
 */
public class RequestBase<D> {

    /**
     * 商家DI
     */
    private String vendorId;


    /**请求路径*/
    private String url;


    /**
     * 请求业务数据
     */
    private D data;


    public D getData() {
        return data;
    }

    public void setData(D data) {
        this.data = data;
    }

    public RequestBase(String vendorId) {
        this.vendorId = vendorId;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
