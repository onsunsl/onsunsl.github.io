"""在TextInput输入焦点有效时候，点击其他控件时候输入框不丢焦点
这个会频繁添加touch 到ignored_touch 该方案不好，
设置TextInput 的unfocus_on_touch = False 即可
"""

from kivy import app
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class IgnoredFocusBehavior(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch not in FocusBehavior.ignored_touch:
                FocusBehavior.ignored_touch.append(touch)
        return super().on_touch_down(touch)


class MyButton(IgnoredFocusBehavior, Button):
    pass


class MyLabel(IgnoredFocusBehavior, Label):
    pass


class MyApp(app.App):
    def build(self):
        box = BoxLayout()
        box.add_widget(TextInput(focus=True))
        box.add_widget(MyLabel(text="Label"))
        box.add_widget(MyButton(text="Button"))
        return box


a = MyApp()
a.run()

