
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from .model import Person


class MainViewModel(EventDispatcher):

    person: Person = ObjectProperty(Person())

    def query(self):
        p = Person()
        p.name = "Liang"
        p.age = 18
        self.person = p
