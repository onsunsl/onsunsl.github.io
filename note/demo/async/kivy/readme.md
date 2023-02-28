### kivy 异步

kivy源码内部底层逻辑和UI都是同步的同步写法，调用，那能不能支持asyncio异步呢？  kivy 内部提供了启动App 的协程，但是仅仅是启动部分， 下面的一个
简单的异步demo

```python
import asyncio
from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        return Button(text="hello")

asyncio.run(MyApp().async_run())
```

这样能保证了主线程都是异步方式调用的，但是为什么内部是同步写法呢？ 那是因为kivy内部全是同步流程，就是：`调用是有结果依赖的`


```python
import asyncio
from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
    async def build(self):
        return await Button(text="hello")
    
asyncio.run(MyApp().async_run())
```

这样的代码会报错误， 因为kivy 内部依赖build 结果是要widget控件，而非coroutine协程
```log
   File "D:\Program Files (x86)\Python38-32-bak\lib\site-packages\kivy\app.py", line 925, in _run_prepare
     raise Exception('Invalid instance in App.root')
 Exception: Invalid instance in App.root
 ```


再看Button的调用例子, Button 的回调写了异步的协程也会报错
```python
import asyncio
from kivy.app import App
from kivy.uix.button import Button

class MyButton(Button):
    async def on_press(self):
        print("MyButton on_press")

class MyApp(App):
    def build(self):
        return MyButton(text="hello")

asyncio.run(MyApp().async_run())
```

说是on_press 没来过会等待他执行完成，因为协程是调用是返回对象而非函数执行结果，awaited是在event loop 里调用的，所以： `但凡kivy 回调处不能写成异步方法`

```log
 D:\Program Files (x86)\Python38-32-bak\lib\site-packages\kivy\uix\behaviors\button.py:151: RuntimeWarning: coroutine 'MyButton.on_press' was never awaited
   self.dispatch('on_press')
 RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

这个也能说明kivy 回调是允许阻塞的，比如调用网络请求都会阻塞而白屏， 处理发方式是： `应用里使用异步写io 阻塞代码，然后在kivy 回调里触发调度`
因为触发调度并不耗时

```python
import functools
import time

from kivy.app import App
from kivy.uix.button import Button
import asyncio
import requests

class MyButton(Button):
    http_task = None

    def data_from_http(self, url):
        r = requests.get(url)
        time.sleep(10)
        print(f"r.status:{r.status_code}")
        if r.status_code == 200:
            return "hell OK"
        else:
            return "hello Error"

    def on_press(self):
        print("MyButton on_press")

        loop = asyncio.get_event_loop()

        async def t():
            fun_with_param = functools.partial(self.data_from_http, "https://www.baidu.com")
            self.text = await loop.run_in_executor(None, fun_with_param)

        loop.create_task(t())


class MyApp(App):
    def build(self):
        return MyButton(text="hello")

asyncio.run(MyApp().async_run())

```

另外一种写法

```python
import asyncio
import aiohttp
from kivy.app import App
from kivy.uix.button import Button


class MyButton(Button):
    http_task = None

    async def http_get(self):
        s = aiohttp.ClientSession()
        r = await s.get("https://www.baidu.com")
        self.text = self.text + f" {r.status}"

    def on_press(self):
        print("MyButton on_press")
        self.http_task and self.http_task.cancel()
        self.http_task = asyncio.create_task(self.http_get())

class MyApp(App):
    def build(self):
        return Button(text="hello")

asyncio.run(MyApp().async_run())

```