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

# 把任务添加到事件循环里
loop.create_task(coroutine, name="helloTask")
print("run forever...")

'''
开始事件循环，这个之后有了输出
run forever...
this hello function

但是结果咱们取呢？
'''
loop.run_forever()
print("the end")
