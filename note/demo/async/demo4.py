import asyncio


async def hello() -> int:
    await asyncio.sleep(2)
    print("this is hello function")
    return 1


loop = asyncio.get_event_loop()
task = loop.create_task(hello(), name="helloTask")
loop.run_until_complete(task)
print(f"hello task result:{task.result()}")
print("the end")


'''
输出结果：
this is hello function
hello task result:1
the end
'''