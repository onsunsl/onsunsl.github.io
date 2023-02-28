import io
import queue
import threading
import time
import traceback
import faulthandler

def f(*args):
    while True:
        t = threading.main_thread()
        faulthandler.dump_traceback()
        print(t.isAlive())
        time.sleep(1)
        print("hello")

cnt = 1
# while True:
#     print(f'hello {cnt}')
#     cnt += 1
#     threading.Thread(target=f).start()
#     queue.Queue().get()
#     time.sleep(10)

import tempfile
with tempfile.TemporaryFile() as f1:
    faulthandler.dump_traceback(f1)
    f1.seek(0)
    for line in f1.readlines():
        print(line)


class _TestHangApp():
    """ 产生测试hang的app窗口进程"""

    # 5秒后模拟hang
    cnt = 5

    def run(self):
        from tkinter import Tk, Label
        lock = threading.Lock()

        def update_ui(_label, *args):
            _TestHangApp.cnt -= 1
            _label.config(text=str(_TestHangApp.cnt))
            _TestHangApp.cnt <= 0 and lock.acquire()
            _label.after(1000, lambda *a: update_ui(_label))

        root = Tk()
        root.title("Test Hang App")
        label = Label(root, bg='yellow', fg='blue', height=5, width=30, font='宋体 10 bold')
        label.pack()
        update_ui(label)
        threading.Thread(target=f).start()
        root.mainloop()


# _TestHangApp().run()