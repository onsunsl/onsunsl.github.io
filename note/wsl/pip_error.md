安装pyqt 错误
```shell
lin@BJ-PF2WYZBP:~$ sudo pip3 install pyqt5 -i https://pypi.douban.com/simple
```

```log
Collecting pyqt5
Using cached https://pypi.doubanio.com/packages/c1/c3/76c52be757e2e07e2f76dfda0e89546a14c1b97004cc7e126851764370b3/PyQt5-5.15.8.tar.gz
Complete output from command python setup.py egg_info:
Traceback (most recent call last):
File "<string>", line 1, in <module>
File "/usr/lib/python3.8/tokenize.py", line 392, in open
buffer = _builtin_open(filename, 'rb')
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pip-build-8wko404l/pyqt5/setup.py'

    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-8wko404l/pyqt5/

```

更新安装
`lin@BJ-PF2WYZBP:~$ sudo pip3 install --upgrade pip setuptools wheel -i https://pypi.douban.com/simple`