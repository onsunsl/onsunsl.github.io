import functools
import logging


def try_times2(n: int):

    def _try_times(fun):
        def inner(*args, **kwargs):
            times = 0
            while times < n:
                try:
                    r = fun(*args, **kwargs)
                    return r
                except Exception as err:
                    print(times)
                    logging.error(f"run {fun} error:{err}", exc_info=True)
                times += 1
        return inner
    return _try_times


@try_times2(3)
def t():
    print(1)
    return 1
t()