import signal

# 在 Windows 上，signal() 调用只能附带 SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, SIGTERM 或 SIGBREAK。
# 任何其他值都将引发 ValueError。 请注意不是所有系统都定义了同样的信号名称集合；
# 如果一个信号名称未被定义为 SIG* 模块层级常量则将引发 AttributeError。
import sys
import time

print(signal.valid_signals())

"""
signal.SIGABRT
来自 abort(3) 的中止信号。

signal.SIGFPE
浮点异常。 例如除以零。


signal.SIGILL
非法指令。

signal.SIGINT
来自键盘的中断 (CTRL + C)。

默认的动作是引发 KeyboardInterrupt。


signal.SIGSEGV
段错误：无效的内存引用。


signal.SIGTERM
终结信号。

signal.SIGBREAK
来自键盘的中断 (CTRL + BREAK)
"""


def on_signal_exit():
    print("on_signal_exit")
    sys.exit(0)


# print(signal.signal(signal.SIGTERM, on_signal_exit))
# for s in signal.valid_signals():
#     print(f"signal:{s}, reg:{signal.signal(s, on_signal_exit)}")

signal.signal(signal.SIGTERM, on_signal_exit)


while True:
    time.sleep(1)
    print("hello")
