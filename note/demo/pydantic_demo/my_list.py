# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : my_list.py
# @Time    : 2022/7/7 16:51
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
import functools
import typing
import pydantic

_T = typing.TypeVar("_T")


def operate(a, b, operator) -> bool:
    a_operator = getattr(a, operator)
    return a_operator(b)


class GenericList(typing.List[_T]):

    # def _operate(self, operator, **fields):
    #     if isinstance(fields, dict) and not fields:
    #         return self.__iter__()
    #
    #     return filter(lambda i: all([operate(getattr(i, n, None), fields[n], operator) for n in fields.keys()]),
    #                   self.__iter__())

    def _operate(self, operator, **fields):
        """根据操作符过滤item"""
        if isinstance(fields, dict) and not fields:
            return list(self.__iter__())

        def op(a, b, _operator) -> bool:
            a_operator = getattr(a, _operator)
            return a_operator(b)

        def match(i) -> typing.Iterable:
            return (op(isinstance(i, dict) and i[n] or getattr(i, n, None), fields[n], operator) for n in fields.keys())

        r = filter(lambda item: all(match(item)), self.__iter__())
        return list(r)

    def eq(self, **fields) -> typing.List[_T]:
        return functools.partial(self._operate, "__eq__")(**fields)

    def ge(self, **fields):
        """Greater than or equal to >= """
        return functools.partial(self._operate, "__ge__")(**fields)

    def gt(self, **fields):
        """Greater than > """
        return functools.partial(self._operate, "__gt__")(**fields)

    def le(self, **fields):
        """Less than or equal to <= """
        return functools.partial(self._operate, "__le__")(**fields)

    def lt(self, **fields):
        """ Less than < """
        return functools.partial(self._operate, "__lt__")(**fields)


class Student(pydantic.BaseModel):
    name: str
    age: int


class StudentList(GenericList[Student]):
    pass


if __name__ == '__main__':

    s = StudentList()


    s.append(Student(name="a", age=12))
    s.append(Student(name="b", age=13))
    s.append(Student(name="b", age=34))

    print("等于12：", s.eq(age=12)[0])
    print("大于12：", list(s.ge(age=12)))
