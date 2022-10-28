# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : demo3.py
# @Time    : 2022/10/27 14:50
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.base import runTouchApp
from kivy.uix.vkeyboard import VKeyboard


class Box(BoxLayout):
    def __init__(self, **kwargs):
        super(Box, self).__init__(**kwargs)
        self.add_widget(TextInput())
        kb = Window.request_keyboard(self._keyboard_close, self)
        if kb.widget:
            self._keyboard = kb.widget
            self._keyboard.layout = "numeric.json"

    def _keyboard_close(self, *args):
        pass

if __name__ == '__main__':
    runTouchApp(Box())
