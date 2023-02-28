import logging

from kivy.clock import Clock
from kivy.core.window.window_sdl2 import WindowSDL
from kivy.core.window import Window
from kivy.uix.button import Button


w = Window
import os

w.add_widget(Button(text="hello"))
Clock.start_clock()
while True:
    Clock.tick()
    Clock.tick_draw()
    w.mainloop()
