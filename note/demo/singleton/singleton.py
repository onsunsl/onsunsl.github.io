import logging
from functools import wraps
from threading import RLock


def singleton(cls):

    inc = dict()
    lock = RLock()

    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls in inc:
            return inc[cls]

        with lock:
            if cls in inc:
                return inc[cls]
            inc[cls] = cls(*args, **kwargs)
            logging.info(f"New {cls.__name__} at {hex(id(inc[cls]))}")

        return inc[cls]
    return _singleton


@singleton
class MyClass(object):

    def __init__(self, value):
        self.value = value
        print(f"第{value}次__init__")


class MyClass2(object):

    def __init__(self, value):
        self.value = value
        print(f"第{value}次__init__")


print(type(MyClass))
print(type(MyClass2))

print(MyClass(1))
print(MyClass(2))
