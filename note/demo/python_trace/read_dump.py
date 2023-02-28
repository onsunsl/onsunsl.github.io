# -*- coding: UTF-8 -*-
import subprocess
import sys
import os

cdb_exe_path = r"cdb.exe"
windows_symbol_path = r"srv*%s*https://msdl.microsoft.com/download/symbols;D:\tools\tools\python366-32with-pdb"


def run_command(sym_path, dmp_file):
    cdb_command = ".reload; !analyze -v;"
    cdb_command += ".printf\"\\n==================== 当前异常现场 ====================\\n\"; .excr;"
    cdb_command += ".printf\"\\n==================== 异常线程堆栈 ====================\\n\"; kv;"
    cdb_command += ".printf\"\\n==================== 所有线程堆栈 ====================\\n\"; ~* kv;"
    cdb_command += "q"
    arguments = [cdb_exe_path, '-z', dmp_file, '-y', sym_path, '-c', cdb_command]
    print(" ".join(arguments))
    output = subprocess.check_output([cdb_exe_path] + arguments)
    print(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        dump_file = r"C:\Users\guanglin.liang\Downloads\SR04022027-wehk328-POS04-20220730\exception.dmp"
    else:
        dump_file = sys.argv[1]

    # os.path.exists(dump_file)
    # dump_file = input()

    run_command(windows_symbol_path, dump_file)
