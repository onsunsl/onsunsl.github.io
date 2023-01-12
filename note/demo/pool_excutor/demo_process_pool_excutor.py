"""
有时需要使用一个线程去执行一个阻塞任务，但是时间会很长， 所以需要设置一个超时时间去关闭它
"""

import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor


class MyProcessPoolExecutor(ProcessPoolExecutor):

    def kill(self):
        for pid, process in self._processes.items():
            print(f"kill {pid}")
            process.kill()


def task(a: int):
    print("start...")
    time.sleep(100)
    return a + 1


if __name__ == '__main__':

    p = MyProcessPoolExecutor(max_workers=1)
    r = p.submit(task, 1)

    try:
        print(r.result(5))
    except Exception as err:
        # p.shutdown(wait=False) # 子进程没有完成会抛异常
        # p.shutdown(wait=True) # 会等子进程完成才退出
        p.kill()

        print("stop")
