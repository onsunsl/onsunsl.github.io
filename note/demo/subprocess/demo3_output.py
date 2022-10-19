import os
import subprocess
import time

import psutil

cmd = ["python", "py_code.py"]
env = os.environ

env["TEST_IP"] = "10.111.87.79"
env["TEST_MAC"] = "10.111.87.79"
env["HANG_DUMP_TEST"] = "-1"
env["PYTHONDEVMODE"] = "1"
env["PYTHONFAULTHANDLER"] = "1"


# 不等待子进程退出
p = subprocess.Popen(cmd, shell=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, universal_newlines=True)
stdout, stderr = p.communicate()
print(stdout)


print("-------")
print(stderr)

print(f"exit code:{p.returncode}")
