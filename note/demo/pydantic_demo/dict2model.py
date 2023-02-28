from typing import List

import pydantic

from note.demo.pydantic_demo.my_list import GenericList


class A(pydantic.BaseModel):
    a: str


class ListA(GenericList[A]):
    pass


class B(pydantic.BaseModel):
    a1: List[A] = pydantic.Field(default_factory=ListA)
    a2: ListA = pydantic.Field(default_factory=ListA)
    b: str


b = B.parse_obj(dict(b="123",
                     a1=[dict(a="aa1"), dict(a="aa2")],
                     a2=[dict(a="aa1"), dict(a="aa2")]))

print(b)
print(b.dict())
