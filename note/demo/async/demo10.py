import multiprocessing
import threading
import asyncio
import time

"""进程、线程各自的event loop"""


async def add(x: int, y: int) -> int:
    y = y * 2
    await asyncio.sleep(1)
    return x * y


async def print_result():
    print(f"add(2, 3): {await add(2, 3)}")


class MyProcess(multiprocessing.Process):

    def run(self):
        loop = asyncio.get_event_loop()
        print(f"SubProcess loop:{id(loop)}")
        asyncio.run(print_result())


class MyThread(threading.Thread):

    async def hello(self) -> int:
        await asyncio.sleep(1)
        print(f"hello")
        await print_result()
        return 1

    def run(self):
        # 这里get的时候夸线程是抛RuntimeError异常
        # loop = asyncio.get_event_loop()
        # 因为协程只能单一线程里工作，所以子线程里只能使用new_event_loop() 创建新的
        loop = asyncio.new_event_loop()
        print(f"SubThread loop:{id(loop)}")

        # run 内部自己独立创建了一个
        asyncio.run(self.hello())


if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    print(f"MainProcess loop:{id(_loop)}")
    t = MyThread()
    t.start()

    p = MyProcess()
    p.start()
    asyncio.run(print_result())
    time.sleep(10)
    print("the end")
