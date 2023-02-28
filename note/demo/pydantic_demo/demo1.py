from decimal import Decimal
from typing import List

from pydantic import (
    BaseModel,
    NegativeFloat,
    NegativeInt,
    PositiveFloat,
    PositiveInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    conbytes,
    condecimal,
    confloat,
    conint,
    conlist,
    conset,
    constr,
    Field,
)

class A(BaseModel):
    a: int  = 1
    b: str = ""


class B(List[A]):

    def filter(self, **fields):
        for i in self.__iter__():
            print(i.a)


b = B()
b.append(A(a=1, b='234'))
b.append(A(a=2, b='456'))

b.filter()