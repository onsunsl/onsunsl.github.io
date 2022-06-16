import time
import socket
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def http_get1(url):
    sock = socket.socket()
    sock.connect((f"{url}", 80))
    req  = f"GET / HTTP/1.0\r\n{url}\r\n\r\n"
    resp = b""
    sock.send(req.encode())
    chunk = sock.recv(4096)
    while chunk:
        resp += chunk
        chunk = sock.recv(4096)
    return resp

def sync_get():
    futures = list()
    workers = 10
    executor = ProcessPoolExecutor(workers)
    task = partial(http_get1, "example.com")
    for _ in range(workers):
        futures.append(executor.submit(task))

    return [f.result() for f in futures]


if __name__ == "__main__":
    begin = time.time()
    print(sync_get()[-1])
    end = time.time()
    print(f"\nsync_get cast: {round(end-begin, 2)}S")