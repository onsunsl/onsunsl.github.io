import os
import subprocess
import time

import psutil

cmd = ["python", "py_code.py"]
env = os.environ

env["TEST_IP"] = "10.111.87.79"
env["TEST_MAC"] = "10.111.87.79"
env["HANG_DUMP_TEST"] = "-1"

# 主进程退后子进程无法使用
f = open("error.log", "w")

# 不等待子进程退出
p = subprocess.Popen(cmd, shell=False, stderr=f, stdout=f, stdin=None, env=env, close_fds=False)
# 等启动(避免子进程起不来)
time.sleep(1)

# 等待子进程退出
# p.wait()

# 等待子进程退出
# subprocess.run(cmd, shell=False, stderr=f, stdout=f, stdin=None, env=env)
# print("exit")
