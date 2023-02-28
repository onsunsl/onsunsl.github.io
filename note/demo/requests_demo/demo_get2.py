# 共用一个连接池
import threading
import time

import requests
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount("http://", HTTPAdapter(pool_connections=1, pool_maxsize=1))


def task(number, *args):
    print(number)
    r = s.get("http://localhost:30000")
    print(r.status_code, r.reason)
    time.sleep(0.1)
    r = s.get("http://localhost:30000")
    print(r.status_code, r.reason)


def task2(number, *args):
    print(number)
    r = s.get("http://localhost:30001")
    print(r.status_code, r.reason)
    time.sleep(0.1)
    r = s.get("http://localhost:30001")
    print(r.status_code, r.reason)


t_list = list()
for i in range(10):
    if i % 2:
        t = threading.Thread(target=task, args=(i, ))
    else:
        t = threading.Thread(target=task2, args=(i, ))
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()

print("end")

