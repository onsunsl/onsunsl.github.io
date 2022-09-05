import enum
import time
import logging
import threading
from typing import Dict, Any

from kivy.clock import Clock
from kivy.app import App


class TaskState(enum.IntEnum):
    """任务状体"""

    CANCEL = 0
    ONCE = 1
    INTERVAL = 2


class Task(object):
    """任务"""

    callback: callable = None
    """任务回调"""

    log: callable = logging.debug
    """任务回调"""

    timeout: float = 0
    """超时时间（超时后调用）"""

    state: TaskState = TaskState.CANCEL
    """任务状体"""

    create_time: float = 0
    """创建时间"""

    def __init__(self, callback: callable, timeout: float, state: TaskState, log: callable = None):
        self.state = state
        self.timeout = timeout
        self.callback = callback
        self.create_time = time.time()
        if callable(log):
            self.log = log

    @property
    def is_timeout(self) -> bool:
        return time.time() > (self.create_time + self.timeout)


class PyKivyClock(object):
    """基于kivy 的UI主线程定时任务调度的python实现"""

    _tasks: Dict[Any, Task] = dict()
    _r_lock = threading.RLock()

    def __init__(self):
        Clock.tick = self._tick

    def _tick(self):
        Clock.pre_idle()
        ts = Clock.time()
        Clock.post_idle(ts, Clock.idle())
        try:
            self._run_task()
        except Exception as err:
            logging.error(err, exc_info=True)

    def _run_task(self):
        remove_list = list()
        logging.debug("开始调度")
        self._r_lock.acquire()
        for name, task in self._tasks.items():
            if not task.is_timeout:
                continue
            begin = time.time()
            try:
                task.log(f"{name}开始")
                task.state and task.callback()
                if task.state == TaskState.INTERVAL:
                    task.create_time = time.time()
                else:
                    remove_list.append(name)
                task.log(f"{name}耗时{time.time()-begin:.2f}S")
            except Exception as err:
                logging.error(f"运行异常:{name}, {err}", exc_info=True)

        for name in remove_list:
            self._tasks.pop(name)
        logging.debug("结束调度")
        self._r_lock.release()

    def _new_task(self, name: str, callback: callable, timeout, state, log):
        self._r_lock.acquire()
        t = Task(callback, timeout, state, log)
        self._tasks[name] = t
        self._r_lock.release()
        return t

    def schedule_once(self, callback: callable, timeout: float = 0.0, name: str = "", log: callable = None):
        name = name or str(callback)
        logging.info(f"{name}添加单次任务, {timeout}S后执行")
        return self._new_task(name, callback, timeout, TaskState.ONCE, log)

    def schedule_interval(self, callback: callable, timeout: float = 0.0, name: str = "", log: callable = None):
        name = name or str(callback)
        logging.info(f"{name}添加循环任务, {timeout}S后执行")
        return self._new_task(name, callback, timeout, TaskState.INTERVAL, log)

    def cancel(self, callback: callable, name: str = "") -> bool:
        name = name or str(callback)
        if name not in self._tasks:
            return False
        logging.info(f"{name}取消任务")
        self._r_lock.acquire()
        self._tasks[name].state = TaskState.CANCEL
        self._r_lock.release()
        return True


PyKivyClockInc = PyKivyClock()


if __name__ == '__main__':

    def fun1(*args):
        print("schedule interval")

    def fun2(*args):
        print("schedule_once")

    PyKivyClockInc.schedule_interval(fun1, timeout=3, log=logging.info)
    PyKivyClockInc.schedule_once(fun2, 2)
    PyKivyClockInc.schedule_once(lambda *a: PyKivyClockInc.cancel(fun1), 10)

    from threading import Thread
    import random

    def cancel(*args):
        while True:
            PyKivyClockInc.cancel(fun1)
            time.sleep(random.random())
            PyKivyClockInc.cancel(fun2)
            time.sleep(random.random())

    def schedule_interval(*args):
        while True:
            PyKivyClockInc.schedule_interval(fun1, random.randint(0, 10), log=logging.info)
            time.sleep(random.random())

    def schedule_once(*args):
        while True:
            PyKivyClockInc.schedule_once(fun2, random.randint(0, 10), log=logging.info)
            time.sleep(random.random())

    Thread(target=schedule_interval).start()
    Thread(target=schedule_once).start()
    Thread(target=cancel).start()
    App().run()
