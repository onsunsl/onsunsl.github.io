import asyncio
import random


async def hello():
    """协程 1"""
    while True:
        print("hello")
        await asyncio.sleep(1)


async def get_number() -> int:
    """ 协程2"""
    await asyncio.sleep(1)
    return random.randint(0, 100)


async def world():
    """协程3"""
    while True:
        number = await get_number()
        task = asyncio.create_task(get_number())
        # await 右边必须是一个可等待的对象，否则会阻塞，如task 是可等待的，而task.result() 是不可等待的
        # number += await task.result()
        number += await task
        print(f"world:{number}")
        await asyncio.sleep(1)


async def main():
    tasks = list()
    tasks.append(asyncio.create_task(hello()))
    tasks.append(asyncio.create_task(world()))
    await asyncio.wait(tasks)


asyncio.run(main())

"""
输出：
hello
hello
hello
world:112
hello
hello
hello
world:109
hello
hello
"""