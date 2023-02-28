from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class A(EventDispatcher):

    a = NumericProperty(0)

    __events__ = ["on_fun1"]

    def __init__(self, **kwargs):
        self.register_event_type('on_test')
        super(A, self).__init__(**kwargs)
        # self.a = 123

    def do_something(self, value):
        # when do_something is called, the 'on_test' event will be
        # dispatched with the value
        self.dispatch('on_test', value)

    def on_test(self, *args):
        print("I am dispatched", args)

    def on_a(self, *args):
        print(f"on_a:{args}")


def my_callback(value, *args):
    print( "Hello, I got an event!", args)


def on_a(*args):
    print(f"on_a outside:{args}")


ev = A()
ev.bind(on_test=my_callback)
ev.do_something('hello')
ev.bind(on_a=on_a)
ev.a = 12321