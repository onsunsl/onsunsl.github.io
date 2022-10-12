
from kivy.uix.screenmanager import Screen

from .load_kv import KvLoad
from .view_model import MainViewModel


class MainWindow(Screen):

    view_model = MainViewModel()

    def __init__(self, **kwargs):
        KvLoad.load(__file__)
        super(MainWindow, self).__init__(**kwargs)
        self.view_model.bind(person=self.on_person)

    def on_person(self, inc, p):
        self.ids.label.text = p.name

    def on_query(self):
        self.view_model.query()
