import faulthandler
import sys
import time
from ctypes import windll
import ctypes.wintypes
import traceback

import atexit

EXCEPTION_CONTINUE_SEARCH = 0


@ctypes.WINFUNCTYPE(ctypes.wintypes.LONG, ctypes.c_void_p)
def crash_handler(c_exception):
    print("----------crash_handler-----------")
    print(c_exception)
    return EXCEPTION_CONTINUE_SEARCH


def python_fault_handler():
    with open("1.dup", 'wb') as f:
        faulthandler.dump_traceback(file=f)
        faulthandler.enable(file=sys.stderr, )
        print(faulthandler.is_enabled())


def set_unhandled_exception_filter():
    """
    这里想在crash_handler 里保存dump但异常都没有调用
    可能是python 强制接管了
    """
    windll.kernel32.SetErrorMode(3)
    windll.kernel32.SetUnhandledExceptionFilter(crash_handler)


@atexit.register
def exit_print():
    print("hello")
    traceback.print_exc()


def call_dll():
    dll = windll.LoadLibrary(r"untitled13/untitled13.dll")
    # 这个是c内存非法访问测试， python 会报 OSError: exception: access violation writing
    dll.mem_test()

    # 这个也是非法内存方法测试
    # import ctypes
    # ctypes.string_at(0)

    # 这个是除0测试， python OSError: exception: integer divide by zero
    # dll.new_obj(0)


if __name__ == '__main__':
    python_fault_handler()
    print(faulthandler.is_enabled())
    set_unhandled_exception_filter()
    call_dll()
