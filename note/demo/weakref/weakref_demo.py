import threading

# 占用大量资源，创建销毁成本很高
class Data:
    def __init__(self, key):
        pass


d = Data("hello")

print(d)

import weakref
rd = weakref.ref(d)
print(rd)

print(rd() is d)

del d

print(rd())
