### 获取python 线程调用栈信息

在定位问题时候python程序运行到哪里是非常重要的信息，在console 运行在异常崩溃时候能输出到console. 
但是如果在其他场景下可能需要记录导致日志方便事后排查

```python
import time
import logging
import threading

def _stack2log(thread_id: int = 0):
    import tempfile
    import faulthandler as fh
    with tempfile.TemporaryFile() as f:
        fh.dump_traceback(f)
        f.seek(0)

        lines = map(lambda l: l.decode().strip(), f.readlines())
        if not thread_id:
            logging.error("\n".join(lines))
            return

        thread_id = f"0x{thread_id:08x}"
        thread_stacks = list()
        for line in lines:
            if not thread_stacks and thread_id not in line:
                continue
            thread_stacks.append(line)
            if line == "":
                break
        logging.error("\n".join(thread_stacks))

```

_stack2log 实现记录指定线程id 的调用栈到log


### 记录线程阻塞位置

```python
import time
import logging
import threading


class ThreadCheck(threading.Thread):

    _last_active: float = None

    _hang_threshold: float = 5.0

    @staticmethod
    def _stack2log(thread_id: int = 0):
        import tempfile
        import faulthandler as fh
        with tempfile.TemporaryFile() as f:
            fh.dump_traceback(f)
            f.seek(0)

            lines = map(lambda l: l.decode().strip(), f.readlines())
            if not thread_id:
                logging.error("\n".join(lines))
                return

            thread_id = f"0x{thread_id:08x}"
            thread_stacks = list()
            for line in lines:
                if not thread_stacks and thread_id not in line:
                    continue
                thread_stacks.append(line)
                if line == "":
                    break
            logging.error("\n".join(thread_stacks))

    @classmethod
    def update_active(cls, hang_threshold: float):
        try:
            if not hang_threshold:
                return
            cls._last_active = time.time()
            cls._hang_threshold = max(float(hang_threshold), 2.0)
        except Exception as err:
            logging.error(f"update_active error:{err}, value:{hang_threshold}")

    def run(self):
        while True:
            try:
                if not self._last_active:
                    return
    
                if abs(time.time() - self._last_active) < self._hang_threshold:
                    return
    
                t = threading.main_thread()
                logging.warning(f"{t.name}@0x{t.ident:08x} hang up {self._hang_threshold}S")
                self._stack2log(t.ident)
            except Exception as err:
                logging.error(f"check error:{err}")
            time.sleep(0.1)

```

其他线程只需要定时调用update_active 即可