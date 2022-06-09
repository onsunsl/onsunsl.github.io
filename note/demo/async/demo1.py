import asyncio
import time


async def hello() -> int:
    """一个协程"""
    await asyncio.sleep(1)
    print("this hello function")
    return 1


# 调用hello
c = hello()
print(f"hello() is：{c}, type:{type(c)}")

print("wait hello... ")
time.sleep(2)
print(f"after hello() is：{c}, type:{type(c)}")


''' 
hello()输出是也给协程类型，不是具体的结果，等待2s 也没有结果，需要event loop 触发才嫩工作
hello() is：<coroutine object hello at 0x03D68AA8>, type:<class 'coroutine'>
wait hello...
after hello() is：<coroutine object hello at 0x03D68AA8>, type:<class 'coroutine'>
sys:1: RuntimeWarning: coroutine 'hello' was never awaited
'''