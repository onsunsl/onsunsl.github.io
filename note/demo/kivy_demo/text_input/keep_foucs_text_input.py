from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

box = BoxLayout()

# 在触摸时候屏幕focus=False, 点击防止TextInput丢焦点
t = TextInput()
t.unfocus_on_touch = False

t2 = TextInput()
t2.unfocus_on_touch = False

box.add_widget(t)
box.add_widget(t2)
box.add_widget(Button(text="button"))
runTouchApp(box)
