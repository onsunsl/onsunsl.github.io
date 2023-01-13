from client import HTTPConnection

c = HTTPConnection("httpbin.org")
c.set_debuglevel(1)
c.request("GET", "/")
resp = c.getresponse()

print(resp.status, resp.reason, resp.version)

print("msg:", resp.msg)
print("header:", resp.headers)
print("body:", resp.read().decode("utf-8"))

