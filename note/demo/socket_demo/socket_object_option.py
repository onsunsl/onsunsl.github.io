import socket

s = socket.socket()

print("默认发送缓冲区长度", s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF))
print("默认接收缓冲区长度", s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF))
print("默认发送超时", s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO))
print("默认接收", s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO))

s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 20)
print("发送缓冲区长度", s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF))
