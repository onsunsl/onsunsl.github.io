import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


class Loop:
    selector = DefaultSelector()
    tasks = list()

    @staticmethod
    def run():
        while Loop.tasks:
            for event_key, event_mask in Loop.selector.select():
                callback = event_key.data
                callback(event_key, event_mask)


class Downloader:

    def __init__(self, url):
        self.url = url
        self.sock: socket.socket = None
        self.resp = B""
        Loop.tasks.append(url)

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(("excample.com", 80))
        except BlockingIOError:
            pass
        Loop.selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        Loop.selector.unregister(key.fd)
        get = f"GET {self.url} HTTP/1.0\r\nHost: example.com\r\n\r\n"
        self.sock.send(get.encode())
        Loop.selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        chunk = self.sock.recv(4096)
        if chunk:
            self.resp += chunk
        else:
            Loop.selector.unregister(key.fd)
            Loop.tasks.remove(self.url)


if __name__ == "__main__":
    import time
    begin = time.time()
    for i in range(10):
        d = Downloader(f"/{i}")
        d.fetch()
    Loop.run()
    end = time.time()
    print(f"\nsync_get cast: {round(end-begin, 2)}S")