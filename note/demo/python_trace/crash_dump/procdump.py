import logging
import os
import subprocess
import datetime

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
        cmd = '"{}/procdump.exe" /accepteula {} "{}"'
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



