import asyncio
import time

import requests
import aiohttp

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor


def get_baidu():
    """同步方式"""
    start = time.time()
    r = requests.get("https://www.baidu.com")
    print(f"get_baidu code:{r.status_code}, cast: {time.time() - start}S")


async def a_get_baidu():
    """异步方式"""
    start = time.time()
    s = aiohttp.ClientSession()
    r = await s.get("https://www.baidu.com")
    print(f"a_get_baidu code:{r.status}, cast: {time.time() - start}S")


async def main():
    loop = asyncio.get_event_loop()
    # run_in_executor 内部默认创建了线程池处理
    coroutines = [a_get_baidu(), loop.run_in_executor(None, get_baidu)]
    await asyncio.gather(*coroutines)

    # 进程池方式处理
    pe = ProcessPoolExecutor(max_workers=1)
    coroutines = [a_get_baidu(), loop.run_in_executor(pe, get_baidu)]
    await asyncio.gather(*coroutines)

if __name__ == '__main__':
    begin = time.time()
    asyncio.run(main())
    print(f"Total cast:{time.time() - begin}S")


'''
总时间接近最长的，但并不是两个加起来
输出：
a_get_baidu code:200, cast: 0.2748899459838867S
get_baidu code:200, cast: 0.3804442882537842S
Total cast:0.3850083351135254S

    # asyncio/base_event.py 里run_in_executor 内部实现
    def run_in_executor(self, executor, func, *args):
        self._check_closed()
        if self._debug:
            self._check_callback(func, 'run_in_executor')
        if executor is None:
            executor = self._default_executor
            if executor is None:
                executor = concurrent.futures.ThreadPoolExecutor()
                self._default_executor = executor
        return futures.wrap_future(
            executor.submit(func, *args), loop=self)

'''