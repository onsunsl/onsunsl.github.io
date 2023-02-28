# -*- coding: gbk -*-
import os
import os.path
import sys
import zipfile
import subprocess


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(sys.executable.encode(encoding))
    return os.path.dirname(os.path.abspath(__file__.encode(encoding)))


def files_in_path(path):
    return list(os.walk(path))[0][2]


def files_filter(filelist, filtertype):
    ''' filtertype = 'zip' filter *.zip files '''
    typelen = len(filtertype) + 1
    return [filename for filename in filelist if '.' + filtertype == filename[-typelen:]]


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def unzip(zipfilelist):
    mkdir(str(module_path(), 'gbk') + '\\dump')
    for files in zipfilelist:
        zfile = zipfile.ZipFile(files, 'r')
        for fileinzip in zfile.namelist():
            data = zfile.read(fileinzip)
            file = open(fileinzip, 'w+b')
            file.write(data)
            file.close()
            os.rename(fileinzip, str(module_path(), 'gbk') + '\\dump\\' + files[:-4] + '.dmp')


def execute_command(command):
    popen = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                             stdout=sys.stdout, stderr=subprocess.STDOUT)
    print(f"run cmd: {command}")
    popen.wait()


if __name__ == '__main__':
    files = files_in_path(str(module_path(), 'gbk'))
    zipfiles = files_filter(files, 'zip')
    unzip(zipfiles)
    mypdbpath = ''
    for line in open("pdbPath.txt"):
        mypdbpath += line.strip()
    mspdbpath = r'SRV*f:\localsymbols*http://msdl.microsoft.com/download/symbols;'
    files = files_in_path(str(module_path(), 'gbk') + '\\dump')
    dumpfiles = files_filter(files, 'dmp')
    for dumpfile in dumpfiles:
        command = "cdb -y " + mspdbpath + mypdbpath + " -z " + "dump\\" + dumpfile + \
                  " -logo " + "dump\\" + dumpfile[:-3] + "txt" + " -lines -c \"!analyze -v;~* kb;q\""
        execute_command(command)

    files = files_in_path(str(module_path(), 'gbk') + '\\dump')
    txtfiles = files_filter(files, 'txt')
    stakereport = open('STACK_TEXT.txt', 'wb+')
    for txtfile in txtfiles:
        needwrite = False
        stakereport.write(bytes(txtfile, 'gbk') + b'\r\n')
        for line in open(str(module_path(), 'gbk') + '\\dump\\' + txtfile, 'rb'):
            # STACK_TEXT:
            if line[:len(b'STACK_TEXT:')] == b'STACK_TEXT:':
                needwrite = True
            if needwrite:
                stakereport.write(line)
            if line[:len(b'\r\n')] == b'\r\n' and needwrite:
                break
