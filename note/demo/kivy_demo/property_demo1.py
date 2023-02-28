# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : property_demo1.py
# @Time    : 2022/9/21 13:41
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------

from kivy import properties
from kivy.event import EventDispatcher
from pydantic import BaseModel


class MyClass(EventDispatcher):

    data = properties.NumericProperty()

    age = properties.NumericProperty()


m = MyClass()
m.fbind("data", lambda *a: print(f"on data {a}"))
m.bind(age=lambda *b: print(f"on age {b}"))
m.data = 123
m.age += 2

print(m.properties())


