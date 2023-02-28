# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : base.py
# @Time    : 2022/7/13 19:55
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
    a: int = pydantic.Field(alias="JsonA")
    b: str = "1"


class B(A):
    @property
    def a(self) -> int:
        return int(self.b)
    b: str = "100"
    c: str = "234"


a = B(JsonA=1, b="234", c="2934")
# print(a.dict(exclude={"b"}))

print(cast(A, a))