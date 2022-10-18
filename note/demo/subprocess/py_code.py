import os
import time

# 测试读写主进程的信息
os.makedirs("test1")

print("from py_code")
print("TEST_IP", os.environ["TEST_IP"])
print("TEST_MAC", os.environ["TEST_MAC"])

time.sleep(10)
print(1/0)
os.makedirs("test")