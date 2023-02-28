# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : demo1.py
# @Time    : 2022/7/7 15:59
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
from typing import List


class A:
    a: int = 1
    b: str = ""


class AList(object):
    _a: List[A] = list()

    # def __iter__(self) -> A:
    #     return self._a.__iter__()
    #
    # def __iter__(self) -> A:
    #     return self._a.__iter__()

    __iter__ = _a.__iter__
    # __next__ = _a.__next__


a = AList()
a._a.append(A())
a._a.append(A())
a._a.append(A())

for i in a:
    print(a.a, a.b)
