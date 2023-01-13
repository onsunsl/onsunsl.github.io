"""
http.client 内部是使用socket.makefile 在HTTPResponse完成接收
下面是一个简单的demo

"""

import socket

host = "www.google.com"
host = "10.12.16.203"
port = 80
port = 30000

HTTP_END_INFO = [b'\r\n', b'\n', b'']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5.0)
# 连接是阻塞的，超时会报： TimeoutError: [WinError 10060]
print(f"连接：{(host, port)}")
s.connect((host, port))

http_msg = f"GET / HTTP/1.1\r\nHost:{host}\r\nConnection:close\r\n\r\n"
print(f"发送：{http_msg}")
s.send(http_msg.encode())

resp = b""

fp = s.makefile("rb")

while True:
    line = fp.readline()
    print(line)
    if line in HTTP_END_INFO:
        print("传输完毕")
        break
