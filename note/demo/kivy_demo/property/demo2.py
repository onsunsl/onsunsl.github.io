import sys

from kivy.clock import Clock
from kivy.properties import DictProperty, ListProperty
from kivy.uix.button import Button
from kivy.base import runTouchApp, stopTouchApp




class MyButton(Button):
    d = DictProperty()
    l = ListProperty()



    def on_l(self, inc, value):
        print(f"list属性响应： {value}")

    def on_d(self, inc, value):
        print(f"dict属性响应： {value}")



    def on_release(self):
        self.d.clear()
        self.l.clear()
        Clock.schedule_once(lambda *args: stopTouchApp(), 1)


if __name__ == '__main__':

    b = MyButton()
    b.l.append(dict(a=1, b=2))
    b.l[0].update(a=123)
    b.l[0]=b.l[0]

    runTouchApp(MyButton())