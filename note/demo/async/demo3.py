import asyncio
import time


async def hello() -> int:
    """一个协程"""
    await asyncio.sleep(1)
    print("this hello function")
    return 1

coroutine = hello()

# 驱动协程的事件循环
loop = asyncio.get_event_loop()

loop.run_until_complete(coroutine)

''' 
hello 会被执行但是并不会执行到这里
因为run_until_complete 参数需要一个Future的对象，而不是coroutine
'''
print("hello is finish")
