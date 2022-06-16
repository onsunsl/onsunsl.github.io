import random
import threading
import time
from socket import socketpair
import socket

a = socket.socketpair()
print(a)

if __name__ == '__main__':
    def runner(*args):
        for _ in range(10):
            result = 0
            for _i in range(100000000):
                result += _i
            print("Thread:{}".format(threading.currentThread()), result)
            time.sleep(random.random())

    for i in range(10):
        print("socketpair")  # 这个后再也没有输出了
        t = threading.Thread(target=runner)
        # asyncio.get_event_loop()  #内部调用了socketpair()
        socketpair()
        t.start()
    print("the end")