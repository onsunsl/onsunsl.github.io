import atexit
import sys
import time

# 程序退出时候回调（杀进程时候无效）
@atexit.register
def goodbye():
    print("exit")


print("hello")
try:
    print(1/0)
except Exception:
    pass


