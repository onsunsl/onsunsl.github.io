from kivy.app import App
from kivy.uix.button import Button
import asyncio
import aiohttp


class MyButton(Button):
    http_task = None

    async def http_get(self):
        s = aiohttp.ClientSession()
        r = await s.get("https://www.baidu.com")
        self.text = self.text + f" {r.status}"

    async def on_press(self):
        print("MyButton on_press")
        self.http_task and self.http_task.cancel()
        self.http_task = asyncio.create_task(self.http_get())


class MyApp(App):

    """ build 会报错 """
    def build(self):
        return MyButton(text="hello")


asyncio.run(MyApp().async_run())
