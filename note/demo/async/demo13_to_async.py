import asyncio
import concurrent.futures.thread
import functools
import time

import requests

g_executor = concurrent.futures.thread.ThreadPoolExecutor()


def to_future(fun):

    def inner(*args, **kwargs):
        loop = asyncio.get_event_loop()
        fun_with_param = functools.partial(fun, *args, **kwargs)
        future_inc = loop.run_in_executor(g_executor, fun_with_param)
        return future_inc
    return inner


@to_future
def get_baidu():
    """同步方式"""
    start = time.time()
    r = requests.get("https://www.baidu.com")
    print(f"get_baidu code:{r.status_code}, cast: {time.time() - start}S")
    return r.status_code


class Demo:
    async def foo(self):
        print("foo...")
        await self.a_block_call()
        self.bar()
        result = await self.get_block_result()
        print(fr"get block result:{result}")

    def bar(self):
        print("bar....")

    @to_future
    def a_block_call(self):
        time.sleep(5)
        print("here is a block call")

    @to_future
    def get_block_result(self):
        time.sleep(4)
        return "block hello"


async def main():
    result = await get_baidu()
    print(fr"get_baidu:{result}")
    await Demo().foo()


asyncio.run(main())
