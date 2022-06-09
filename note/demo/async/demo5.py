import asyncio


async def hello(name: str) -> str:
    print(f"hello_{name} is running...")
    await asyncio.sleep(2)
    print(f"hello_{name} done")
    return f"hell_{name}"


loop = asyncio.get_event_loop()


tasks = [loop.create_task(hello("3")), loop.create_task(hello("4"))]
asyncio.wait(tasks)
loop.run_forever()
