from kivy.clock import Clock

from kivy.app import App

def fun(*args):
    print("schedule_interval")
    return True

e = Clock.schedule_interval(fun, 1)


App().run()