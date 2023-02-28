"""
在很多时候会使用到类似urllib, requests, urllib3 http客户端库，但是这几个库底层都来自同一个连接入口`socket.create_connection`
方法，而这个方法内部实现了：域名解析`socket.getaddrinfo`、创建socket对象、设置超时时间、连接域名对应的主机的工作
而域名解析getaddrinfo是一个阻塞的接口， 如果赞系统底层解析不到域名对应的ip, 会连接DNS服务器解析，但是这个方法没有超时的参数，导致整个上层的
应用阻塞。

解决方案：
实现一个非阻塞且带缓存的getaddrinfo

参考：
requests timeout无效  https://www.jianshu.com/p/4a82ece96eaa
requests库卡在getaddrinfo做dns查询  https://blog.csdn.net/sumousguo/article/details/82662678
浅谈getaddrinfo函数的超时处理机制 https://blog.csdn.net/Javin_L/article/details/82627560
"""


import time
import socket
import _socket
from concurrent.futures import ProcessPoolExecutor


class MyProcessPoolExecutor(ProcessPoolExecutor):

    def kill(self):
        for pid, process in self._processes.items():
            print(f"kill pid: {pid}")
            process.kill()


class AddressInfo(object):
    """非阻塞域名解析"""

    cache_timeout: int = 60 * 60 * 8
    """解析缓存超时时长"""

    block_time: int = 5
    """单次解析阻塞时长"""

    address_cache: dict = dict()
    """解析缓存"""

    @classmethod
    def init(cls, cache_timeout: int = 60 * 60 * 8, block_time: int = 5):
        """
        初始化
        :param cache_timeout: 缓存保持时长(S)
        :param block_time:    单次解析等待时间（S）
        :return: 无
        """
        cls.timeout = cache_timeout
        cls.block_time = block_time
        socket.getaddrinfo = cls.get_address_info

    @staticmethod
    def block_get_address(host, port, family=0, t_type=0, proto=0, flags=0):
        """阻塞调用系统解析DNS接口"""
        addrlist = []
        for res in _socket.getaddrinfo(host, port, family, t_type, proto, flags):
            af, sock_type, pt, canon_name, sa = res
            addrlist.append((AddressInfo._converter(af, socket.AddressFamily),
                             AddressInfo._converter(sock_type, socket.SocketKind),
                             pt, canon_name, sa))
        return addrlist

    @classmethod
    def get_address_info(cls, host, port, family=0, t_type=0, proto=0, flags=0):
        """带超时和缓存实现socket.getaddrinfo功能"""
        req = (host, port, family, t_type, proto, flags)
        key = str((host, port, family, t_type, proto, flags))
        if key not in cls.address_cache:
            return cls._address_info_with_timeout(*req)
        save_time, address_info = cls.address_cache.get(key)
        if cls._is_timeout(save_time):
            cls.address_cache.pop(key)
            print(f"从缓存解析:{host} 已经失效")
            return cls._address_info_with_timeout(*req)

        print(f"从缓存解析:{host} -> {address_info}")
        return address_info

    @classmethod
    def _is_timeout(cls, save_time: int):
        return save_time + cls.cache_timeout < time.time()

    @classmethod
    def _converter(cls, value, enum_klass):
        try:
            return enum_klass(value)
        except ValueError:
            return value

    @classmethod
    def _address_info_with_timeout(cls, host, port, family=0, t_type=0, proto=0, flags=0):
        """进程带超时执行解析"""
        e = MyProcessPoolExecutor(max_workers=1)
        f = e.submit(cls.block_get_address, host, port, family, t_type, proto, flags)
        result = f.result(timeout=cls.block_time)
        e.kill()

        print(f"从系统解析:{host} -> {result}")
        key = str((host, port, family, t_type, proto, flags))
        if result:
            cls.address_cache[key] = time.time(), result
        return result


if __name__ == '__main__':
    AddressInfo.init()
    print(socket.getaddrinfo("baidu.com", 80)[-1])
    print(socket.getaddrinfo("baidu.com", 80)[-1])
    print(socket.getaddrinfo("google.cc", 80)[-1])
    print(socket.getaddrinfo('110.242.68.66', 80)[-1])

    for info in socket.getaddrinfo("localhost", 80):
        print(info)
    for info in socket.getaddrinfo("localhost", 80):
        print(info)
    import requests
    r = requests.get("https://www.baidu.com")
    print(r.status_code)
    print(r.reason)

    print(f"socket.getaddrinfo:{socket.getaddrinfo}")
