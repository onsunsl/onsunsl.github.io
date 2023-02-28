import gc

# kivy 的clock定时器
from kivy.clock import Clock


class ClockTest:

    def __init__(self):

        def call2(*args):
            print(f"call2")

        # 在Clock 启动时候立即调用call2
        Clock.schedule_once(call2)

        # 在Clock 启动时候立即调用self.call
        Clock.schedule_once(self.call)

    def call(self, *args):
        print("call....")


ClockTest()

# 上面的ClockTest实例被释放
gc.collect()

# 触发定时调用
Clock.tick()


"""
输出只有：call2 调用了， call 并没有调用

分析：
  1.kivy内部默认不对call做引用计数增加（其实是做了弱引用）， ClockTest()类的实例被释放时候， 所以对象的call方法没有调用
  2.call2 在python c底层是一个独立的类型，只是这个实例化了这个对象被 ClockTest()类 实例引用了，然后也kivy 内部做了弱引用

"""
