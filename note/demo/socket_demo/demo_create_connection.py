"""
在http.client 标准库模块内部使用了socket.create_connection创建链接
而socket 链接create_connection内部使用了set_timeout， 但是时间的连接超时时间跟操作系统有关
windows 最长时间为21.26秒， 所以在windows 下连接超时参数取值范围为0~21的整数


create_connection内部做了几件事：
 - 根据传入的host和port 调用socket.getaddrinfo自动解析ip、协议族类型AF_INET和传输类型SOCK_STREAM, 但是是阻塞的
 - 根据解析结果创建socket对象
 - settimeout设置超时
 - 连接成功返回sock对象

"""

import socket
import time
import traceback

begin = time.time()
try:
    print(f"链接开始")
    s = socket.create_connection(("google.cc", 80), timeout=5)
except Exception as err:
    print(f"链接异常：{err}")
    print(traceback.format_exc())
finally:
    print(f"链接耗时：{time.time()-begin:.2f}")


"""原有的写法"""
timeout = 5
host, port = ("google.cc", 80)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(timeout)
s.connect((host, port))




