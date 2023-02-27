package com.hello.http;

import com.alibaba.fastjson.JSON;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class HttpClient {


    public static String api;

    public static <REQ, RESP> ResponseBase<RESP> request(RequestBase<REQ> request, Class<RESP> classResp)
    {
        ResponseBase<RESP> response = new ResponseBase<>();
        String result = postJson(api+request.getUrl(), JSON.toJSONString(request));
        response.setCode(200);
        response.setMsg("查询成功");

        String dataStr = "{\"id\": \"123\", \"name\": \"hello\"}";
        response.setData(JSON.parseObject(dataStr, classResp));

//        RESP data = "{\"id\": \"123\", \"name\": \"hello\"}";
//        RESP data = new UserInfoResponse();
//        response.setData(new RESP());
        return response;
    }

    public static String postJson(String httpUrl, String param) {

        HttpURLConnection connection = null;
        InputStream inputStream = null;
        OutputStream outputStream = null;
        BufferedReader bufReader = null;
        String result = null;
        try {
            URL url = new URL(httpUrl);
            // 通过远程url连接对象打开连接
            connection = (HttpURLConnection) url.openConnection();
            // 设置连接请求方式
            connection.setRequestMethod("POST");
            // 设置连接主机服务器超时时间：15000毫秒
            connection.setConnectTimeout(15000);
            // 设置读取主机服务器返回数据超时时间：60000毫秒
            connection.setReadTimeout(60000);

            // 默认值为：false，当向远程服务器传送数据/写数据时，需要设置为true
            connection.setDoOutput(true);
            // 默认值为：true，当前向远程服务读取数据时，设置为true，该参数可有可无
            connection.setDoInput(true);
            // 设置传入参数的格式:请求参数应该是 name1=value1&name2=value2 的形式。
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

            
            // 通过连接对象获取一个输出流
            outputStream = connection.getOutputStream();
            // 通过输出流对象将参数写出去/传输出去,它是通过字节数组写出的
            outputStream.write(param.getBytes());
            // 通过连接对象获取一个输入流，向远程读取
            if (connection.getResponseCode() == 200) {

                inputStream = connection.getInputStream();
                // 对输入流对象进行包装:charset根据工作项目组的要求来设置
                bufReader = new BufferedReader(new InputStreamReader(inputStream, "UTF-8"));

                StringBuffer strBuf = new StringBuffer();
                String temp = null;
                // 循环遍历一行一行读取数据
                while ((temp = bufReader.readLine()) != null) {
                    strBuf.append(temp);
                    strBuf.append("\r\n");
                }
                result = strBuf.toString();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 关闭资源
            if (null != bufReader) {
                try {
                    bufReader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if (null != outputStream) {
                try {
                    outputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if (null != inputStream) {
                try {
                    inputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            // 断开与远程地址url的连接
            if (null!=connection) {
                connection.disconnect();
            }
        }
        return result;
    }

}
