"""tab键切换input控件的光标"""

from kivy import app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyTextInput(BoxLayout):
    """自定义input控件"""

    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.add_widget(Label(text="user"))
        self.add_widget(TextInput(write_tab=False, text="MyTextInput"))


class MyApp(app.App):
    def build(self):
        box = BoxLayout()

        t1 = TextInput(write_tab=False)
        t2 = TextInput(write_tab=False)
        t3 = MyTextInput()

        box.add_widget(t1)
        box.add_widget(t2)
        box.add_widget(t3)
        return box


a = MyApp()
a.run()

