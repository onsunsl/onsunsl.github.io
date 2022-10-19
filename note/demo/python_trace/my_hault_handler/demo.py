import os
import time
from multiprocessing import Process

import faulthandler2


def hello(*args, **kwargs):
    code = args[0]

    print(f"----{code} {args}, {kwargs}")


f = open("1.txt", "a")

print("enable:", faulthandler2.enable(file=f, all_threads=True))
print("pid:", os.getpid())
print(time.time())
print(faulthandler2.is_enabled())


class CustomerProcess(Process):

    def run(self):
        print(f"sub pid:{os.getpid()}, ppid:{os.getppid()}")
        import ctypes
        ctypes.string_at(0)

        while True:
            time.sleep(1)


if __name__ == '__main__':

    CustomerProcess().start()

    for i in range(2):
        time.sleep(1)

    try:
        import ctypes
        ctypes.string_at(0)
    except BaseException as e:
        print(e)
        # print(traceback.format_exc())
    print("the end")
