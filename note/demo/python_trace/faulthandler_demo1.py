import time

import faulthandler
import traceback

if __name__ == '__main__':
    f = open("1.txt", "w")

    faulthandler.enable(f)
    print(faulthandler.is_enabled())

    try:
        import ctypes
        ctypes.string_at(0)
    except BaseException as e:
        print(e)
        print(traceback.format_exc())
    print("the end")
