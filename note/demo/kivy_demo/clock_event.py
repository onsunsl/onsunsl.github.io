import gc

from kivy.clock import Clock
from functools import partial


class ClockTest:

    def __init__(self):
        self.a = [1, 2]

        def call2(*args):
            """function class """
            print(self.a[1])
            print("call2....")

        e = Clock.create_trigger(self.call, release_ref=True)
        e()
        Clock.schedule_once(call2)

    def call(self, *args):
        print("call....")


class Counter:
    def call(self, *args, **kwargs):
        # nonlocal value
        value = 42
        print("-----call-----------")


def test_clock_event_trigger_ref(kivy_clock):
    value = None



    event = kivy_clock.create_trigger(lambda *_: Counter().call())
    gc.collect()
    event()
    kivy_clock.tick()
    # assert value is None
    print("1")

    event = kivy_clock.schedule_once(Counter().call)
    event()
    kivy_clock.tick()
    # assert value is None
    print("2")

    event = kivy_clock.create_trigger(Counter().call, release_ref=True)
    gc.collect()
    event()
    kivy_clock.tick()
    # assert value == 42
    print("3")


test_clock_event_trigger_ref(Clock)
# ClockTest()
# gc.collect()
# Clock.tick()

