urllib3 

urllib 是python内置的http客户端的库（urllib 和urllib2都是）
urllib3 是第三方实现类似urllib的库，它比urllib更强大

urllib3具有如下优点：

* 支持HTTP和SOCKS代理
* 支持压缩编码
* 100%测试覆盖率
* 具有链接池
* 线程安全
* 客户端SLL/TLS验证
* 协助处理重复请求和HTTP重定位
* 使用multipart编码上传文件

urllib3 是第三方库需要自己安装， 但是如果安装requests库是会自动安装
简单使用:
```python
import urllib3
m = urllib3.PoolManager()
r = m.request("GET", "http://www.baidu.com")
print(r.status)
```


### 1.连接池`PoolManager`
连接池是管理所有的url主机连接




### 参考

[urllib3库详解](https://www.cnblogs.com/KGoing/p/6146999.html)
