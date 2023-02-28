import sys


class Sign(object):

    sign_cmd = r"D:\tools\sign_tool\Signtool.exe sign /f D:\tools\sign_tool\dmall.pfx /p dmall.com /t http://timestamp.digicert.com /d DMallOS /v {}"

    def run_windows_cmd(self, cmd_list: list):
        import subprocess

        for cmd in cmd_list:
            print("Run cmd:{}".format(cmd))
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            p.wait()
            err = stdout and stdout.decode("GBK") or ""
            info = stderr and stderr.decode("GBK") or ""
            info and print(info)
            if err:
                print(err)
                return False
        else:
            _ = self
        return True

    def sign(self, file: str):
        cmd = self.sign_cmd.format(file)
        self.run_windows_cmd([cmd])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        exe_file = sys.argv[1]
    else:
        exe_file = input("请输入待签名文件完整路径：")
    Sign().sign(exe_file)
    input()
