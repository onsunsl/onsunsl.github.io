# -*- coding: utf-8 -*-
# @Project : onsunsl.github.io
# @Author  : GuangLin
# @File    : demo.py
# @Time    : 2022/6/7 17:05
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------

from abc import ABC
from typing import Generic, TypeVar, List

T = TypeVar("T")


class MyQueue(ABC, Generic[T]):
    """一个泛型Q"""
    def __init__(self) -> None:
        self.items: List[T] = list()

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop(0)


if __name__ == '__main__':
    q = MyQueue[int]()

    # 这里运行并没有报错
    q.push("123")
    q.push(123)
    print(q.pop())
    print(q.pop())
