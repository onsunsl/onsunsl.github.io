import time

import urllib3

import urllib
import urllib.request

r = urllib.request.Request("http://www.baidu.com")
r = urllib.request.Request("http://www.google.com")

begin = time.time()
try:
    resp = urllib.request.urlopen(r, timeout=1)
    print(resp.status)
    print(resp.msg)
except Exception as err:
    print(f"error:{err}")
finally:
    print(f"cast_time:{time.time()-begin:.2f}S")

