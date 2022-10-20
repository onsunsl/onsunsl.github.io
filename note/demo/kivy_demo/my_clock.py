import re
import enum
import time
import logging
import threading
from typing import Dict, Any

from kivy.clock import Clock


class TaskState(enum.IntEnum):
    """任务状态"""

    CANCEL = 0
    ONCE = 1
    INTERVAL = 2


class Task(object):
    """任务"""

    name: str = ""
    """名称"""

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

    def __init__(self, name: str, callback: callable, timeout: float, state: TaskState, log: callable = None):
        self.name = name
        self.state = state
        self.timeout = timeout
        self.callback = callback
        self.create_time = time.time()
        if callable(log):
            self.log = log
        else:
            self.log = lambda *args: None
        self.log(f"创建{self}")

    def __str__(self):
        return f"{self.name} {self.state.name} {self.timeout}S"

    @property
    def is_timeout(self) -> bool:
        return time.time() > (self.create_time + self.timeout)

    def cancel(self):
        self.log(f"取消{self}")
        self.state = TaskState.CANCEL


class PyKivyClock(object):
    """基于kivy 的UI主线程定时任务调度的python实现"""

    _tasks_running: Dict[Any, Task] = dict()
    """运行中任务列表"""

    _tasks_new: Dict[Any, Task] = dict()
    """新创建任务列表"""

    _r_lock = threading.RLock()
    """列表锁"""

    _is_running = False
    """是否在运行"""

    _enable: bool = False
    """PyKivyClock开关"""

    _instance: "PyKivyClock" = None
    """全局唯一实例"""

    _logger: logging.Logger = None
    """本模块logger"""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._r_lock:
                if not cls._instance:
                    cls._instance = object.__new__(cls)
                    cls._logger = logging.getLogger("PyKivyClock")
                    cls._logger.setLevel("INFO")
        return cls._instance

    def _tick(self):
        try:
            Clock.pre_idle()
            ts = Clock.time()
            Clock.post_idle(ts, Clock.idle())
            self._enable and self._run_task()
        except Exception as err:
            logging.error(err, exc_info=True)

    async def _async_tick(self):
        Clock.pre_idle()
        ts = Clock.time()
        current = await Clock.async_idle()
        Clock.post_idle(ts, current)
        self._enable and self._run_task()

    def _run_task(self):
        self._logger.debug(f"开始调度：{len(self._tasks_running)}")
        self._r_lock.acquire()
        self._is_running = True
        cancel_list = list()
        for name, task in self._tasks_running.items():
            if not task.is_timeout:
                continue

            try:
                if task.state != TaskState.CANCEL:
                    begin = time.time()
                    task.log(f"{name}开始")
                    if TaskState.CANCEL == task.callback():
                        task.state = TaskState.CANCEL
                    task.log(f"{name}耗时{time.time()-begin:.2f}S")

                if task.state == TaskState.INTERVAL:
                    task.create_time = time.time()
                else:
                    cancel_list.append(name)
            except Exception as err:
                self._logger.error(f"运行异常:{name}, {err}", exc_info=True)

        # 调度同时UI操作增加任务,追加到running列表里
        newest = dict(filter(lambda i: i[1].state, self._tasks_new.items()))
        if newest:
            self._tasks_running.update(newest)
            self._logger.info(f"追加:{len(newest)}")
        self._tasks_new.clear()

        # 从running删除取消的
        for name in cancel_list:
            self._tasks_running.pop(name)
        self._logger.debug("结束调度")
        self._is_running = False
        self._r_lock.release()

    @staticmethod
    def _get_name(callback: callable, name: str):
        t = int(time.time() * 1000)
        try:
            if name:
                return f"{name}-{t}"
            if hasattr(callback, "__name__"):
                return callback.__name__
            name = str(callback)
            res = ["(?<=bound method )(.+?)(?= of )", ]
            for r in res:
                result = re.findall(r, name)
                if result:
                    return f"{result[0]}-{t}"
            return f"{name}-{t}"
        except Exception as err:
            PyKivyClock._logger.error(err, exc_info=True)
            return f"Unknown-{t}"

    def _new_task(self, name: str, callback: callable, timeout, state, log) -> Task:
        """创建任务
            -多线程下通过锁互斥访问任务
            -主线程会同时响应kivy touch和clock事件，需要_is_running状态同步任务
        """
        self._logger.info("开始创建任务")
        self._r_lock.acquire()
        t = Task(name, callback, timeout, state, log)
        if self._is_running:
            self._tasks_new[name] = t
        else:
            self._tasks_running[name] = t
        self._r_lock.release()
        self._logger.info(f"结束任务创建:{t}")
        return t

    @property
    def enable(self) -> bool:
        return self._enable

    @enable.setter
    def enable(self, value: bool):
        if isinstance(value, bool):
            self._enable = value
            self._logger.warning(f"自定义clock开关：{self._enable}")
        else:
            self._logger.error("enable必须是bool类型")

        if self._enable:
            Clock.tick = self._tick
            Clock.async_tick = self._async_tick

    @property
    def log_level(self) -> int:
        return self._logger.level

    @log_level.setter
    def log_level(self, value):
        if isinstance(value, (str, int)):
            self._logger.setLevel(value)
        else:
            self._logger.error("log_level必须是str或int类型")

    def schedule_once(self, callback: callable, timeout: float = 0.0, name: str = "", log: callable = None) -> Task:
        if self._enable:
            name = self._get_name(callback, name)
            return self._new_task(name, callback, timeout, TaskState.ONCE, log)
        else:
            return Clock.schedule_once(callback, timeout)

    def schedule_interval(self, callback: callable, timeout: float = 0.0, name: str = "", log: callable = None) -> Task:
        if self._enable:
            name = self._get_name(callback, name)
            return self._new_task(name, callback, timeout, TaskState.INTERVAL, log)
        else:
            return Clock.schedule_interval(callback, timeout)


