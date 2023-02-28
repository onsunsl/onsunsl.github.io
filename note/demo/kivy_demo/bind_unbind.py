from kivy import app
from kivy.uix.button import Button


class MyApp(app.App):

    def on_release(self, *args):
        print(*args)

    def on_release2(self, *args):
        print(2, *args)


    def on_state(self, *args):
        print(*args)

    def on_state2(self, *args):
        print(2, *args)

    def build(self):
        b = Button(text="Button")
        # print(b.bind(on_release=self.on_release))
        # print(b.unbind(on_release=self.on_release))
        # b.bind(on_release=self.on_release2)
        # print(b.get_property_observers("release"))
        # b.bind(state=self.on_state)
        print(b.get_property_observers("state"))
        # b.fbind(state=self.on_state2)
        return b

a = MyApp()
a.run()

