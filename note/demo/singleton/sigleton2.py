import functools
import threading


class SingletonBase(object):

    _instance = None
    _lock = threading.RLock()
    _is_create = True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        else:
            cls._is_create = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if self._is_create:
            self._on_create(*args, **kwargs)

    def _on_create(self, *args, **kwargs):
        pass

    @classmethod
    def instance(cls):
        if cls._instance:
            return cls._instance
        else:
            return cls.__new__()


class MyClass0:
    def __init__(self, *args, **kwargs):
        print("MyClass0", args, kwargs)


class MyClass(SingletonBase, MyClass0):

    # def __init__(self, value, *args, **kwargs):
    #     self.value = value
    #     print(f"第{value}次__init__")
    #     SingletonBase.__init__(self, *args, **kwargs)

    def _on_create(self, *args, **kwargs):
        print("_on_create sub:", *args, **kwargs)
        MyClass0.__init__(*args, **kwargs)



print(MyClass)
print(MyClass(1))
print(MyClass(2))
