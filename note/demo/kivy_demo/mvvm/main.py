from kivy.app import App
from asyncio import get_event_loop

from app.view import MainWindow


class MyApp(App):

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    app = MyApp()
    loop = get_event_loop()
    loop.run_until_complete(app.async_run())
    loop.close()
