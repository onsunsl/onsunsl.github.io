import time

print("A crash app starting...")
import ctypes
time.sleep(20)
print("make a crash...")
ctypes.string_at(0)


