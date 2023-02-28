import gc

from kivy.clock import Clock
from functools import partial


class ClockTest:

    def __init__(self):
        self.a = [1, 2]

        def call2(*args):
            print(self.a[1])
            print(f"call2")

        Clock.schedule_once(self.call)
        Clock.schedule_once(call2)

    def call(self, *args):
        print("call....")


ClockTest()
gc.collect()
Clock.tick()


"""
输出：
call....
2
call2

分析：
  call2内部对ClockTest 的成员a引用，所以ClockTest的对象不会在手动扫描gc时候释放, 所以call 和call2都会调用

"""
