from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class IconButton(Button):

    def __init__(self, **kwargs):

        text = kwargs.pop("text", "")
        box = BoxLayout()
        label = Label(text=text)
        box.add_widget(label)
        box.add_widget(label)

