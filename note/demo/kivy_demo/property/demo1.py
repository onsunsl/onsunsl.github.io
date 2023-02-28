import sys

from kivy.clock import Clock
from kivy.properties import DictProperty, ListProperty
from kivy.uix.button import Button
from kivy.base import runTouchApp, stopTouchApp

dd = dict(a=1, sub=dict(bb=123))


class MyButton(Button):
    d = DictProperty()
    l = ListProperty()

    e = None

    def on_l(self, inc, value):
        print(f"list属性响应： {value}")

    def on_d(self, inc, value):
        print(f"dict属性响应： {value}")

        # 这里的修改回导致重复触发on_d调用
        # value["b"] = 2

        # 这里修改不回到触发on_d调用， 但是回修改外面的dd和内部d
        # 因为dd和内部d 都引用了dd["sub"]
        # value["sub"]["bb"] = 234

        print(f"属性响应内部修改后： {value}")

        # self.e = value
        # print(f"e: {self.e}, d:{self.d}")

    def on_release(self):
        # del self.d
        # del self.e
        self.d.clear()
        self.l.clear()
        Clock.schedule_once(lambda *args: stopTouchApp(), 1)


if __name__ == '__main__':
    print(f"赋值前引用dd：{sys.getrefcount(dd)}, {sys.getrefcount(dd['sub'])},  id:{id(dd)}")
    b = MyButton()
    b.d = dd
    print(f"赋值kivy后dd的值:{dd}")
    print(f"赋值后引用dd：{sys.getrefcount(dd)}, {sys.getrefcount(dd['sub'])},  id:{id(dd)}")

    runTouchApp(MyButton())
    print(b.d, b.e)
    del b

    # print(f"id(b): {id(b)}")
    import gc

    print("gc.get_referents", gc.get_referents(dd['sub']))
    print("gc.get_referents", gc.get_referrers(dd['sub']))
    print(f"赋值后引用dd：{sys.getrefcount(dd)}, {sys.getrefcount(dd['sub'])},  id:{id(dd)}")
