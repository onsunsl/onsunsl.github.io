"""
这里使用普通Button 模拟键盘事件直接发送到Window层
on_textinput 是 SDL 图形库需要的机制，所以当你的windows
实现层用的是SDL 时候on_textinput 事件是必须的

虽然可以继承VKeyboard 和配置对应的layout的json 但是对
单个按键的图片资源并不可配置， 所以 可以使用普通button 的方式

关于可key_code参考：kivy/core/window/__init.py
关于scan_code参考：https://www.weizhuannet.com/p-9206656.html
"""

from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button


class MyButton3(Button):

    def __init__(self, **kwargs):
        self.key_code = kwargs.pop("key_code", 0)
        self.scan_code = kwargs.pop("scan_code", 0)
        self.key_value = kwargs.pop("key_value", "")
        super(MyButton3, self).__init__(**kwargs)

    def on_release(self):
        if self.key_value:
            Window.dispatch("on_textinput", self.key_value)

    def on_state(self, btn, state):
        if self.state == 'down':
            Window.dispatch("on_key_down", self.key_code, self.scan_code, self.key_value, [])
        else:
            Window.dispatch('on_key_up', self.key_code, self.key_value)


box = BoxLayout()

# unfocus_on_touch 是点击按钮时候保持textinput的焦点
t = TextInput(unfocus_on_touch=False)
box.add_widget(t)

# 可显示的按键
box.add_widget(MyButton3(text="1", key_value="1", key_code=49, scan_code=30))

# 功能键 回车
box.add_widget(MyButton3(text="Enter", key_value="", key_code=13, scan_code=30))

# 功能键 功能键table
box.add_widget(MyButton3(text="Tab", key_value="", key_code=9, scan_code=30))

# 功能键 功能键退格
box.add_widget(MyButton3(text="Backspace", key_value="", key_code=8, scan_code=30))

runTouchApp(box)
