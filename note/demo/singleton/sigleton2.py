import threading


class SingletonBase(object):

    _lock = threading.RLock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance


class MyClass(SingletonBase):

    def __init__(self, value):
        self.value = value
        print(f"第{value}次__init__")


print(MyClass(1))
print(MyClass(2))
