# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : demo4_dymatc.py
# @Time    : 2022/7/20 11:31
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
from typing import cast

import pydantic


class A(pydantic.BaseModel):
    a: int
    b: int
    value: int
    value_name: str = "a"

    def __setattr__(self, key, value):
        value_name: ""


a = B(JsonA=1, b="234", c="2934")
# print(a.dict(exclude={"b"}))

print(cast(A, a))