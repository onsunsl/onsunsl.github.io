

from kivy import app
from kivy.uix.button import Button

class MyButton(Button):

    def on_text(self, *args):
        print("------------->", args)

    def on_release(self):
        self.text = "hello"


class MyApp(app.App):
    def build(self):
        b = MyButton(text="Button")
        setattr(b, "text", "world")
        return b


a = MyApp()
a.run()

