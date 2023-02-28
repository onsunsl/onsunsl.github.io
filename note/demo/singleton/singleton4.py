class Singleton(type):

    _inc = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inc:
            cls._inc[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._inc[cls]


class MyClass2:

    def __init__(self, value):
        self.value = value
        print(f"第{value}次__init__")


class MyClass(MyClass2, metaclass=Singleton):

    def __init__(self, value):
        self.value = value
        print(f"第{value}次__init__")
        super(MyClass, self).__init__(value)



print(type(MyClass))
print(type(MyClass2))
print(MyClass(1))
print(MyClass(2))
