
class Task:
    def __init__(self, coroutine):
        self.coroutine = coroutine
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coroutine.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


def connect(sock, host):
    f = Future()
    sock.setblocking(False)
    try:
        sock.connect(host)
    except BlockingIOError:
        pass

    def on_connected():
        f.set_result(None)

    Loop.selector.register(sock.fileno(), EVENT_WRITE, on_connected)
    yield from f
    Loop.selector.unregister(sock.fileno())


def read(sock):
    f = Future()

    def on_readable():
        f.set_result(sock.recv(4096))

    Loop.selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield from f
    print("Loop.selector.unregister(sock.fileno())", chunk)
    Loop.selector.unregister(sock.fileno())
    return chunk

def read_all(sock):
    resp = b""
    chunk = yield from read(sock)
    while chunk:
        resp += chunk
        chunk = yield from read(sock)


import socket

class Download:
    def __init__(self, url):
        self.url = url
        self.resp = b""

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        yield from connect(sock, ("example.com", 80))
        get = f"GET {self.url} HTTP/1.0\r\nHost: example.com\r\n\r\n"
        sock.send(get.encode())
        self.resp = yield from read_all(sock)
        if self.url in Loop.tasks:
            Loop.tasks.remove(self.url)

import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

class Future:
    def __init__(self):
        self.result = None
        self._callbacks = list()

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        yield self
        return self.result


class Loop:
    selector = DefaultSelector()
    tasks = list()

    @staticmethod
    def run():
        while Loop.tasks:
            events = Loop.selector.select()
            for event_key, event_mask in events:
                callback = event_key.data
                callback()

if __name__ == "__main__":
    import time
    begin = time.time()
    for url in range(10):
        url = f"/{url}"
        Loop.tasks.append(url)
        d = Download(url)
        Task(d.fetch())

    Loop.run()
    print(f"yield cast:{time.time() - begin}")