from client import HTTPConnection

c = HTTPConnection("httpbin.org")
c.request("GET", "/")
resp = c.getresponse()

print(resp.status, resp.reason, resp.version)

print("msg:", resp.msg)
print("body:", resp.read().decode("utf-8"))

