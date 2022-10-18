import os
import subprocess
import time

import psutil

cmd = ["notepad.exe", "StartFromPython"]
env = os.environ

env["TEST_IP"] = "10.111.87.79"
env["TEST_MAC"] = "10.111.87.79"
env["HANG_DUMP_TEST"] = "-1"

p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE, stdin=subprocess.PIPE, cwd=r"D:/", env=env)
# p.wait()


print("pid:{}".format(p.pid))


while True:
    ps = psutil.Process(p.pid)
    if ps.children():
        print(ps.children(), ps.children()[0].pid)
    time.sleep(1)
