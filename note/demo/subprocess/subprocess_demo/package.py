import shutil
import subprocess

import PyInstaller.__main__ as py_installer

from sign import Sign

py_installer.run(["update.py", "-y",  "-w", "--log-level=DEBUG"])
py_installer.run(["main.py", "-y",  "-w", "--log-level=DEBUG"])
Sign().sign("./dist/main.exe")
Sign().sign("./dist/update.exe")
Sign().sign("./dist/main/main.exe")
Sign().sign("./dist/update/update.exe")
shutil.copy("./dist/update/update.exe", "./dist/main/")
