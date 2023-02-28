from kivy.event import EventDispatcher
from kivy.app import App
from kivy.properties import ListProperty

class MyEventDispatcher(EventDispatcher):

    data = ListProperty()



def my_callback(value, *args):
    print("Hello, I got an event!", args)


ev = MyEventDispatcher()
ev.bind(data=my_callback)

ev.data.append(123)
# a = App()
#
# a.run()

