import os
import time
from multiprocessing import Process

import faulthandler2

"""
保持异常时候的调用栈： 类似内存非法访问的异常try except 也能捕获，但是fault handler 是兜底方案
C 层面实现记录：异常时间、进程和线程栈， 支持多进程但是file参数需要以`a`追加方式打开

"""


def hello(*args, **kwargs):
    code = args[0]

    print(f"----{code} {args}, {kwargs}")


f = open("1.txt", "a")

print("enable:", faulthandler2.enable(file=f, all_threads=True))
print("pid:", os.getpid())
print(time.time())
print(faulthandler2.is_enabled())


class CustomerProcess(Process):
    """子进程异常示例"""

    def run(self):
        print(f"sub pid:{os.getpid()}, ppid:{os.getppid()}")
        try:
            # 这里不捕获异常程序将退出
            import ctypes
            ctypes.string_at(0)
        except Exception as err:
            print(f"CustomerProcess error: {err}")


if __name__ == '__main__':

    CustomerProcess().start()

    for i in range(2):
        time.sleep(1)

    try:
        # 这里不捕获异常程序将退出
        import ctypes
        ctypes.string_at(0)
    except BaseException as e:
        print(e)
        # print(traceback.format_exc())
    print("the end")
