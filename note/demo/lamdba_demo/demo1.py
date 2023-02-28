import functools


def fun():

    print(lambda a: print(a))
    return lambda a: print(1)

def fun2():

    print(lambda b: print(b+2))
    return lambda b: print(1)

print(fun())
print(fun2())

f = fun()
print(f.__class__)
# print(f.__self__) 没有self
print(f.__class__.__name__)

f = functools.partial(fun)
print(f.__class__)
print(f.__class__.__name__)
# print(f.__self__) 没有self


def fun3(f):
    if f.__self__ is not None:
        print("not none")
    else:
        print(f.__func__.__name__)
        print(f.__self__)

fun3(lambda b: print(123))