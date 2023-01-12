import random
import socket
import threading
import time


def addr_info(*args):
    for i in range(1000):
        time.sleep(random.random())
        print(i, socket.getaddrinfo("google.com", 80))


t_list = list()
for i in range(10):
    t = threading.Thread(target=addr_info)
    t.start()
    t_list.append(t)

for t in t_list:
    t.join()
print("done")
