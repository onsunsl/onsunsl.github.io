"""等待"""

import asyncio


def get_time() -> int:
    return 5


async def hello():
    await asyncio.sleep(get_time())
    print("hello")


async def world():
    await asyncio.sleep(1)
    print("world")


async def main():
    try:
        # 等待单个协程，必须带吃时间
        print("wait for single coroutine:")
        await asyncio.wait_for(hello(), 2)
    except asyncio.TimeoutError:
        print(f"timeout error")

    # 等待多个协程
    print("wait single coroutines:")
    await asyncio.wait({hello(), world()})

    # 等待多个任务
    print("wait single tasks:")
    await asyncio.wait({asyncio.create_task(hello()), asyncio.create_task(world())})

asyncio.run(main())
