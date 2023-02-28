import httpx
r = httpx.get("https://www.baidu.com")
print(r.status_code)

