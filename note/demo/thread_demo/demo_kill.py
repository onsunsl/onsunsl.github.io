import threading
import time


def task(*args):
    print("start...")
    time.sleep(1000)


t = threading.Thread(target=task)
t.start()
print(t.is_alive())
