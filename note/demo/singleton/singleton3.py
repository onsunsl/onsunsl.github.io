import functools


class Singleton:

    def __init__(self, func):
        self._fun = func

    @functools.wraps
    def __call__(self, *args, **kwargs):
        return self._fun(*args, **kwargs)



@Singleton
class MyClass(object):

    def __init__(self, value):
        self.value = value
        print(f"第{value}次__init__")


print(type(MyClass))

# print(MyClass())
# print(MyClass())



