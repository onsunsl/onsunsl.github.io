import functools
import time

from kivy.app import App
from kivy.uix.button import Button
import asyncio
import requests

class MyButton(Button):
    http_task = None

    def http_get(self, url):
        time.sleep(10)
        return requests.get(url)

    async def update_txt(self):
        loop = asyncio.get_event_loop()
        # r = await loop.run_in_executor(None, requests.get, "https://www.baidu.com")
        r = await loop.run_in_executor(None, self.http_get, "https://www.baidu.com")
        print(f"r.status:{r.status_code}")
        if r.status_code == 200:
            self.text = "hell OK"
        else:
            self.text = "hello Error"

    def on_press(self):
        print("MyButton on_press")
        loop = asyncio.get_event_loop()
        loop.create_task(self.update_txt())


class MyApp(App):
    def build(self):
        return MyButton(text="hello")


asyncio.run(MyApp().async_run())
