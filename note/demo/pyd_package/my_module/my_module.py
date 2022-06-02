from my_module.sub_folder import sub_module


def hello() -> None:
    print("hello " + sub_module.world())


def py_fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = a + b, a
    return a


if __name__ == '__main__':
    hello()
