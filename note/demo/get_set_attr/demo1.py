"""
初衷： 为了解决对成员属性读写访问的控制， 如果合法性控制。避免if else 判断
什么是描述符？ 类里实现了__get__, __set__, __delete__ 任意一个

利用描述可以实现: classmethod、staticmethod、property 等装饰器
参考:https://zhuanlan.zhihu.com/p/196473543
"""


class Score(object):

    def __init__(self, value):
        self._value = value

    def __get__(self, instance, owner):
        print("get value")
        return self._value

    def __set__(self, instance, value):
        print("set value")
        if not isinstance(value, (float, int)):
            raise TypeError("Score must be number")
        if not 0 <= value <= 100:
            raise ValueError("value  must be 0 to 100")
        self._value = value


class Student(object):

    chinese = Score(0)
    english = Score(0)
    math = Score(0)

    def __init__(self, name, c, e, m):
        self.name = name
        self.math = m
        self.chinese = c
        self.english = e

    def __str__(self):
        return f"Student {self.name}, chinese:{self.chinese}, english:{self.english}, math:{self.math}"

    def __getattribute__(self, item):
        print(f"__getattribute__:{item}")
        return super(Student, self).__getattribute__(item)


if __name__ == '__main__':

    s = Student("Lin", 90, 80, 90)
    print(s)
