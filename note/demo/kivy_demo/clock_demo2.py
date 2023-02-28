from kivy.clock import Clock

from kivy.app import App

e = Clock.schedule_once(lambda *_: print("call..."))
e.cancel()
e()

App().run()