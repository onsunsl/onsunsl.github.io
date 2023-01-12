import socket
import time

"""
/* s.settimeout(timeout) method.  Argument: socket对象在py层暴露的settimeout接口，参数：
   None -- no timeout, blocking mode; same as setblocking(True)    阻塞模式用不超时，它和setblocking(True)一样
   0.0  -- non-blocking mode; same as setblocking(False)           非阻塞模式，它和setblocking(False)一样
   > 0  -- timeout mode; operations time out after timeout seconds 超时模式，指定时间(秒)内没有成功会引发timeout异常
   < 0  -- illegal; raises an exception                            小于0抛异常
*/


"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
timeout内部初始化是：-1 * 1000 * 1000 * 1000
- gettimeout() 时候做转换 timeout < 0 返回None, 其他是setimeout()时的值
- setblock(True) timeout=0
- setblock(False) timeout=-1
"""
# --------------------------- 默认阻塞模式 ---------------------------
print("默认超时时间:", s.gettimeout())

# ----------------------------- 超时模式 ---------------------------
s.settimeout(1)
print("设置超时时间:", s.gettimeout())

begin = time.time()
try:
    s.connect(("10.12.16.203", 30000))
except Exception as err:
    print(f"链接错误:{err}")
finally:
    print(f"耗时:{time.time() - begin:.2f}S")
    s.close()

# ----------------------------- 非阻塞模式 ---------------------------
# 会立刻抛异常， 所以应该配合select模块使用

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0)
print("设置超时时间:", s.gettimeout())

begin = time.time()
try:
    s.connect(("10.12.16.203", 3000))
except Exception as err:
    print(f"链接错误:{err}")
finally:
    print(f"耗时:{time.time() - begin:.2f}S")
    s.close()

s.recv
