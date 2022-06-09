import asyncio

'''
协程调用链
'''


async def world() -> str:
    print("world")
    await asyncio.sleep(1)
    return "world"


async def hello():
    print("hell")
    await asyncio.sleep(1)

    print("hello " + await world())


asyncio.run(hello())

"""
输出：
hell
world
hello world
"""