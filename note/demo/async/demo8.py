"""
协程并发
"""

import asyncio


async def foo():
    await asyncio.sleep(1)
    print("do something in foo")


async def bar():
    for i in range(4):
        await asyncio.sleep(1)
        print(f"do something in bar:{i}")


async def main():
    tasks = [foo(), bar()]
    await asyncio.gather(*tasks)


asyncio.run(main())
print("the end")
