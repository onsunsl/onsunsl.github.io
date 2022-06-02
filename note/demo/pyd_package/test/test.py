import time

from my_module import my_module, c_fib, pyx_fib


def fib_test():

    my_module.hello()
    n = 10000
    m = 1000

    begin = time.time()
    for _ in range(m):
        r = pyx_fib.fib(n)
    print("pyx_fib.fib() cast:{}S".format(time.time() - begin))

    begin = time.time()
    for _ in range(m):
        r = c_fib.c_fib(n)
    print("c_fib.fib() cast:{}S".format(time.time() - begin))

    begin = time.time()
    for _ in range(m):
        r = my_module.py_fib(n)
    print("my_module.py_fib cast:{}S".format(time.time() - begin))

    print("the end")


if __name__ == '__main__':
    fib_test()
