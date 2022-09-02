import logging
import queue
import threading
import time
from functools import partial
from typing import Dict, Any

from kivy.clock import Clock

from kivy.app import App


class Task(object):

    callback: callable = None
    """任务回调"""

    timeout: int = 0
    """超时时间（超时后调用）"""

    is_interval: bool = False

    create_time: int = 0

    def __init__(self, callback: callable, timeout: int, is_interval: bool):
        self.callback = callback
        self.timeout = timeout
        self.is_interval = is_interval
        self.create_time = time.time()

    @property
    def is_timeout(self) -> bool:
         return time.time() > self.create_time + self.timeout



class MyKivyClock():

    _tasks: Dict[Any, Task]  = dict()

    _r_lock = threading.RLock()

    def _new_task(self, name: str, callback: callable, timeout: int = 0, is_interval=False):
        if name in self._tasks:
            logging.warning("覆盖已存在任务")
            self._tasks.pop(name)
        timeout = int(time.time() + timeout)
        self._tasks[name] = Task(callback, timeout, is_interval)
        logging.info(f"done")

    def once_task(self, callback: callable, timeout: int = 0, name: str = ""):
        name = callback.__name__ or name
        logging.info(f"添加单次任务:{name}, {timeout}S")
        return self._new_task(name, callback, timeout, False)

    def interval_task(self, callback: callable, timeout: int = 0, name: str = ""):
        name = callback.__name__ or name
        logging.info(f"添加循环任务:{name}, {timeout}S")
        return self._new_task(name, callback, timeout, False)

    def cancel_task(self,  callback: callable, name: str = "") -> bool:
        name = callback.__name__ or name
        logging.info(f"取消任务：{name}")
        if name not in self._tasks:
            return False
        self._tasks.pop(name)
        return True

    def _run_task(self):
        remove_list = list()
        for name, task in self._tasks.items():
            if not task.is_timeout:
                continue
            try:
                task.callback()
            except Exception as err:
                logging.error(f"运行异常:{name}, {err}", exc_info=True)
            if task.is_interval:
                task.create_time = time.time()
            else:
                remove_list.append(name)

        for name in remove_list:
            self._tasks.pop(name)

    def tick(self):
        Clock.pre_idle()
        ts = Clock.time()
        Clock.post_idle(ts, Clock.idle())
        self._run_task()

e = Clock.schedule_once(lambda *_: print("call..."))



App().run()