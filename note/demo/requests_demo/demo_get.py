import time

import requests

"""
get 请求：

* requests.get
* requests.request <- "GET"  
    * 创建Session对象，内部会创建http和https的请求适配器HTTPAdapter实例
    * HTTPAdapter主要是实现发送和关闭， 构造时候创建连接池子对象PoolManager

* 调用Session.request
    * 调用session的send
    * 转发到adapter.send
        * 从poolmanager对象的connection_from_url获取连接
            * 从poolmanager.connection_from_host获取连接
                * 从poolmanager.connection_from_context获取连接  根据主机域名、端口、http/https作上下文
                    * 从poolmanager.connection_from_pool_key获取连接  
                      * 根据主机域名、端口、http/https、请求参数等生成PoolKey对象做key
                      * 从poolmanager.pool中取可以对应的连接 / 不存在创建一个新的连接
                        * 从HTTPConnectionPool 对象里创建连接池对象
            

"""

# 独立连接池

r = requests.get("http://www.baidu.com")

print(r.status_code, r.reason)

time.sleep(4)

r = requests.get("http://www.baidu.com")

print(r.status_code, r.reason)

print("-----------------")

# 共用一个连接池
s = requests.Session()

r = s.get("http://www.baidu.com")
print(r.status_code, r.reason)

time.sleep(4)

r = s.get("http://www.baidu.com")
print(r.status_code, r.reason)
time.sleep(1)

r = s.get("http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=a&fenlei=256&oq=sadfas&rsv_pq=8d959cc20000554a&rsv_t=3f6bLpWPQQR%2FaqXXCcqYUo6YA1IP05aWHlbD2SZk%2BgAsZQQYoouHPbBwjCg&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&inputT=1057&rsv_sug3=8&rsv_sug1=4&rsv_sug7=100&rsv_sug4=1057")
print(r.status_code, r.reason)
time.sleep(1)

r = s.get("http://map.baidu.com/@12952530,4838630,13z")
print(r.status_code, r.reason)


