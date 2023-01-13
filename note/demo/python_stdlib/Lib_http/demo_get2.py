import client

c = client.HTTPConnection("httpbin.org")
c.set_debuglevel(1)
c.request("GET", "/get?name=GL&age=25")
resp = c.getresponse()

print(f"响应状态码:{resp.status}, 错误消息：{resp.reason}, http版本：{resp.version}")
print("响应头:", resp.msg)
print("返回数据：", resp.read().decode("utf-8"))

c.close()

