import gc
import sys
import threading

import weakref


class Data:
    """数据缓存"""
    def __init__(self, _key):
        pass


class Cache:
    """数据缓存"""
    def __init__(self):
        # WeakKeyDictionary：当key没有引用时候，会自动删除对应的key和value
        self.pool = weakref.WeakKeyDictionary()
        self.lock = threading.Lock()

    def get(self, _key):
        with self.lock:
            data = self.pool.get(_key)
            if data:
                print("from cache")
                return data

            print("create")
            data = Data(_key)
            print(sys.getrefcount(data))

            # 这个只缓存了data 的弱引用（不做计数增加）
            self.pool[_key] = data
            print(sys.getrefcount(data))
            return data


key = "hello"

c = Cache()

# 第一次获取创建新的
d = c.get(key)

# sys.getrefcount(d) 时候会增加计数， 返回后释放
print(sys.getrefcount(d))

print(d)
print(c.get(key))
print(c.get(key) is d)
print(sys.getrefcount(d))

print("\nafter release:")
key = None

# 修改d 或 del d 会做减计数， 而释放d, 再次获取的时候为None
print(c.get(key))
print(c.get(key) is d)

