import time

from client import  HTTPConnection

host1 = "www.google.com"

# 默认阻塞链接
# c = HTTPConnection(host1, port=30000)
# begin = time.time()
# try:
#     print(f"默认阻塞链接开始")
#     c.connect()
# except Exception as err:
#     print(f"链接异常：{err}")
# finally:
#     print(f"默认阻塞链接耗时：{time.time()-begin:.2f}")
#     c.close()

host2 = "baidu.com"
c = HTTPConnection(host2, port=80, timeout=2000)
begin = time.time()
try:
    print(f"链接开始")
    c.connect()
except Exception as err:
    print(f"链接异常：{err}")
finally:
    print(f"链接耗时：{time.time()-begin:.2f}")

    try:
        begin = time.time()
        c.sock.recv(1000)
    except Exception as err:
        print(f"接收异常：{err}")
    finally:
        print(f"接收耗时：{time.time()-begin:.2f}")
c.close()


