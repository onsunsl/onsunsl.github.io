import asyncio
import time
from asyncio import Future


async def world():
    await asyncio.sleep(4)
    print("world")
    return "world"


def hello():
    print("hello")
    t = asyncio.create_task(world())
    while not t.done():
        continue
    print(t.result())
    print("world completed")


async def do_exit():
    print("do exit....")
    await asyncio.sleep(4)


async def main():
    print("main")
    hello()
    await do_exit()

asyncio.run(main())
