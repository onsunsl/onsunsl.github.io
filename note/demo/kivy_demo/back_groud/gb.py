import os

import kivy.app
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen



class MyBoxLayout(BoxLayout):



    def image(self, file):
        return os.path.join(os.getcwd(), file)

Builder.load_file("./bg.kv")
#
# Builder.load_string(
# """
# MyBoxLayout:
#     BoxLayout
#         canvas.before:
#             Color:
#                 rgba: 1,0, 0,1
#             Rectangle:
#                 pos: self.pos
#                 size: self.size
#                 source: root.image("cart_left_bg.png")
#
#         BoxLayout:
#             canvas.before:
#                 Rectangle:
#                     pos: self.pos
#                     size: self.size
#                     source: root.image("frame34a710x150.png")
#
#         BoxLayout:
#             canvas.before:
#                 Rectangle:
#                     pos: self.pos
#                     size: self.size
# """
# )

class MyApp(kivy.app.App):
    def build(self):
        return MyBoxLayout()


a = MyApp()
a.run()

