import logging
import os
import subprocess
import datetime

class ACrashApp():

    def run(self):
        p = subprocess.Popen("python a_crash_app.py", stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,  cwd=os.getcwd())
        return p


class Dump:
    @staticmethod
    def save_dump(pid: int, dump_file: str, cwd: str = ".") -> None:
        """
        通过进程ID判断是否是无响应
        @param pid       窗口句柄ID
        @param dump_file 保存dump文件
        @param cwd       工作路径
        @return None
        """
        cmd = '"{}/procdump.exe" /accepteula {} -e "{}"'
        try:
            if "{}" in dump_file:
                now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                dump_file = dump_file.format(now)

            if not os.path.exists(os.path.dirname(dump_file)):
                os.makedirs(os.path.dirname(dump_file))

            if os.path.exists(dump_file):
                os.remove(dump_file)
            cmd = cmd.format(cwd or os.getcwd(), pid, dump_file)
            print("运行dump命令: {}".format(cmd))
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE,  cwd=os.getcwd())
            p.wait()
            stdout = p.stdout.read()
            stdout and print("stdout: {}\n".format(stdout.decode("gbk")))
            stderr = p.stderr.read()
            stderr and print("stderr: {}\n".format(stderr.decode("gbk")))
        except Exception as err:
            print("运行命令 {} error：{}".format(cmd, err))


p = ACrashApp().run()
Dump.save_dump(p.pid, "./output/test.dmp")


"""
运行dump命令: "./procdump.exe" /accepteula 25028 -e "./output/test.dmp"
stdout:
ProcDump v10.11 - Sysinternals process dump utility
Copyright (C) 2009-2021 Mark Russinovich and Andrew Richards
Sysinternals - www.sysinternals.com

Process:               python.exe (25028)
Process image:         D:\Program Files (x86)\Python38-32\python.exe
CPU threshold:         n/a
Performance counter:   n/a
Commit threshold:      n/a
Threshold seconds:     n/a
Hung window check:     Disabled
Log debug strings:     Disabled
Exception monitor:     Unhandled
Exception filter:      [Includes]
                       *
                       [Excludes]
Terminate monitor:     Disabled
Cloning type:          Disabled
Concurrent limit:      n/a
Avoid outage:          n/a
Number of dumps:       1
Dump folder:           D:\onsunsl.github.io\note\demo\python_trace\procdump\output\
Dump filename/mask:    test
Queue to WER:          Disabled
Kill after dump:       Disabled


Press Ctrl-C to end monitoring without terminating the process.

[09:10:20] Exception: C0000005.ACCESS_VIOLATION
[09:10:20] The process has exited.
[09:10:20] Dump count not reached.

python 解释器崩溃后procdump无法捕获
"""


