import wrapt
from kivy.app import App
from kivy.uix.button import Button
import asyncio
import aiohttp


import asyncio

import wrapt


class async_event_no_overlap:
    """转换成异步事件并阻止重复触发。"""

    _running: bool = False
    """是否执行中？"""

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        if self._running:
            return

        asyncio.get_running_loop().create_task(self._call(wrapped, instance, args, kwargs))

    async def _call(self, wrapped, instance, args, kwargs):
        self._running = True
        try:
            await wrapped(*args, **kwargs)
        finally:
            self._running = False


def async_event_no_overlap1(fun):

    async def _call(_fun, self, *args, **kwargs):
        if getattr(self, "__running__", False):
            return
        setattr(self,  "__running__", True)
        await _fun(self, *args, **kwargs)
        setattr(self,  "__running__", False)

    def inner(*args, **kwargs):
        asyncio.get_running_loop().create_task(_call(fun, *args, **kwargs))
    return inner


class MyButton(Button):
    http_task = None

    async def http_get(self):
        s = aiohttp.ClientSession()
        r = await s.get("https://www.example.com")
        self.text = self.text + f" {r.status}"

    @async_event_no_overlap1
    async def on_press(self):
        print("MyButton on_press")
        # self.http_task and self.http_task.cancel()
        # self.http_task = asyncio.create_task(self.http_get())


class MyApp(App):
    def build(self):
        return MyButton(text="hello")


asyncio.run(MyApp().async_run())
