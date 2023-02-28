from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang.builder import Builder


class MyLabel(Label):
    pass


class MyApp(App):

    def build(self):
        from my_class import MyClass
        print(MyClass.text)
        return MyLabel()


if __name__ == '__main__':
    from kivy.factory import Factory
    from my_class import MyClass

    Factory.register("MyClass", MyClass)
    # Factory.register("MyClass", )
    Builder.load_string("""
#:import MyClass my_class.MyClass
<MyLabel>:
    text: getattr(MyClass, "text")
""")

    app = MyApp()
    app.run()
