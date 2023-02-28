

from kivy import app
from kivy.uix.button import Button


class MyApp(app.App):
    def build(self):
        return Button(text="Button")


a = MyApp()
a.run()

