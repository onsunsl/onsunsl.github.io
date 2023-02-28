import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

class Loop:
    selector = DefaultSelector()
    tasks = list()

    @staticmethod
    def run():
        while Loop.tasks:
            for event_key, event_mask in Loop.selector.select():
                callback = event_key.data
                callback()

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

class Download:
    def __init__(self, url):
        self.url = url
        self.resp = b""

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(("excample.com", 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected():
            f.set_result(None)

        Loop.selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        Loop.selector.unregister(sock.fileno())
        get = f"GET {self.url} HTTP/1.0\r\nHost: example.com\r\n\r\n"
        sock.send(get.encode())

        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            Loop.selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            Loop.selector.unregister(sock.fileno())
            # print(f"reade {self.url}:{chunk}")
            if chunk:
                self.resp += chunk
                continue
            if self.url in Loop.tasks:
                Loop.tasks.remove(self.url)


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
