from kivy import app
from kivy.uix.button import Button


class MyButton(Button):

    def on_release(self):
        from kivy.core.audio.audio_sdl2 import SoundSDL2
        p = SoundSDL2(source='./beep.mp3')
        p.play()


class MyApp(app.App):
    def build(self):
        return MyButton(text="Button")


a = MyApp()
a.run()
