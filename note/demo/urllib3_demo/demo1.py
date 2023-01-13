import urllib3
from urllib3._collections import RecentlyUsedContainer

# 带线程安全、容量可控、删除回调类有序字典的容器, 是PoolManager内部连接池使用的容器
r = RecentlyUsedContainer(2, lambda *args: print(f"pop {args}"))
r.update(a=123)
r.update(b=456)

# a = 123 被清理
r.update(c=789)
print(dict(r))

# c = 789被清理
r.update(c=444)
print(dict(r))


m = urllib3.PoolManager()
r = m.request("GET", "http://www.baidu.com")
print(r.status)
