# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : alias_json_name.py
# @Time    : 2022/7/13 15:29
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
import pydantic


class A(pydantic.BaseModel):
    a: int = pydantic.Field(alias="JsonA")
    b: str = "1"


a = A.parse_obj({"JsonA": 123})
print(a.dict(exclude={"b"}))

print(a)