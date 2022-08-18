import datetime
import faulthandler
import io
import os
import time

from note.demo.python_trace.crash_dump.procdump import Dump


def a_crash_fun():
    print("A crash app starting...")
    import ctypes
    time.sleep(1)
    print("make a crash...")
    ctypes.string_at(0)


class MyFile(io.FileIO):
    def write(self, *args, **kwargs):
        print("--------------------------")
        print(args, kwargs)
        # super(MyFile, self).write(*args, **kwargs)


try:
    # f = open(f"./fault_handler.log", "a+")
    # f.write(f"\n\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} App start..\n")
    f = MyFile("1.log", "w")
    if not faulthandler.is_enabled():
        print("Enable fault handler")
        faulthandler.enable(f)
    a_crash_fun()
except:
    # import traceback
    # print(traceback.format_exc())
    # Dump.save_dump(os.getpid(), "./output/test.dmp")
    pass
