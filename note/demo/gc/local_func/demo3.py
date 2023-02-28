import gc

from kivy.clock import Clock
from functools import partial


class ClockTest:

    def __init__(self):
        self.a = [1, 2]

        def call2(*args):
            print(self.a[1])
            print(f"call2")

        Clock.schedule_once(call2)
        Clock.schedule_once(self.call)

    def call(self, *args):
        print("call....")


ClockTest()
gc.collect()
Clock.tick()


"""
输出：
2
call2

分析：
  call2内部对ClockTest 的成员a引用，调用了call2 后释放所以ClockTest()对象销毁，所以没有掉用call

"""
