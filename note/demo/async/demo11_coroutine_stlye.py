import asyncio


async def do_nothing():
    """协程"""
    pass


async def average():
    """async + yield是异步生成器"""
    total = 0.0
    count = 0
    avr = 0
    while True:
        # yield 左边item 是接收值 / 右边avr, total是返回值
        item = yield avr, total
        total += item
        count += 1
        avr = total / count


async def grouper():
    """ 协程 """
    avr = average()
    nothing = do_nothing()
    print(f"average() type is :{avr}")
    print(f"do_nothing() type is :{nothing}")

    # 这里需要触发一次，把第一次调用到yield位置返回值丢弃
    await avr.asend(None)
    for i in range(10):

        # 发送并接收
        a, t = await avr.asend(i)
        print(f"total:{t}, var:{a}")

asyncio.run(grouper())
