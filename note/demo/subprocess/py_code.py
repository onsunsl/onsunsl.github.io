import faulthandler
import os
import signal
import sys
import time

print("from py_code")
print("TEST_IP", os.environ["TEST_IP"])
print("TEST_MAC", os.environ["TEST_MAC"])

time.sleep(1)

def handler(*args, **kwargs):
    print(f"-----{args}, {kwargs}")

signal.signal(signal.SIGTERM, handler)

# 记录调用回调
# def trace(frame, event, arg):
#     print ("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
#     return trace
#
# sys.settrace(trace)

import ctypes
ctypes.string_at(0)

while True:
    time.sleep(1)
    print("test")