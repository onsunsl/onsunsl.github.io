from abc import ABC
from typing import TypeVar, Generic

import pydantic
import asyncio
from abc import ABC
from asyncio import AbstractEventLoop
from typing import Awaitable, Callable, Generic, Optional, TypeVar

from reactivex import abc, from_future
from reactivex import operators as rxops
from reactivex.subject import BehaviorSubject

_T = TypeVar("_T")
_TResult = TypeVar("_TResult")


class MyModel(pydantic.BaseModel):

    data: list = pydantic.Field(default_factory=list)


class ReactiveModel(ABC, Generic[_T]):
    """反应式模型。"""

    _subject: BehaviorSubject[_T]
    """主题。"""

    def __init__(self, value: _T):
        self._subject = BehaviorSubject(value)

    def value(self) -> _T:
        """获取model实例"""
        return self._subject.value

    def select(self) -> abc.ObservableBase[_T]:
        return self._subject

    def set_value(self, value: _T):
        self._subject.on_next(value)


class ViewModel(ReactiveModel[MyModel]):
    def __init__(self, *args):
        super().__init__(MyModel())


v = ViewModel()
v.select().subscribe(on_next=lambda a: print(a))

d = v.value()
d.data.append("123")
v.set_value(d)


d = v.value()
d.data[0] = "456"
v.set_value(d)

print("exit")
