requests 库 是一个很优秀的http客户端库，方法简洁简单

requests 底层是调用的urllib3实现的， urllib3实现了基于http类型（http/https）、域名、端口为key 的
连接池索引， 而连接池实现了多线程下同时访问一个主机的连接管理，默认但线程

简单的demo:
```python
import requests

r = requests.get("http://www.baidu.com")
print(r.reason, r.status_code)
```

它的请求路径如下: 
-> requests.get() 
-> Session().request() 
-> HTTPAdapter().send() 
-> PoolManager()connection_from_url() 
-> HTTPConnectionPool().urlopen() 
-> HTTPConnection().request() 
-> http.HTTPConnection().request()