from kivy import properties
from kivy.event import EventDispatcher
from pydantic import BaseModel


class MyClass(EventDispatcher):

    data = properties.ListProperty()


m = MyClass()
m.bind(data=lambda *b: print(f"on data {b}"))

m.data.append(123)
m.data.append(456)
del m.data[:]
print(m.data)

print(m.properties())


