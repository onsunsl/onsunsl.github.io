pyqtdeploy-sysroot --target android-64 --source-dir sources/ --source-dir D:/Qt/5.15.2 --verbose sysroot.json

需要安装: [perl](https://strawberryperl.com/) 用来配置openssl源码

* Qt报错
> Qt: verifying...
> pyqtdeploy-sysroot: Qt: v5.15.2 is specified but the host installation is v5.6.3.
这个是检查Qt 版本时候报错, Qt 目录需要设置到path, pyqtdeploy的Qt.py 对检查Qmake.exe的版本

* Python 报错

Python: verifying...
pyqtdeploy-sysroot: Python: installing the host Python from a source package on Windows is not supported.

sysroot.toml 文件配置windows 都不从源码安装
```toml
# Python ######################################################################

[Python]
version = "3.8.10"
install_host_from_source = false

[Python.win]
install_host_from_source = false
```


### 参考：
[PyQtdeploy-V2.4 User Guide 中文 （一）](https://www.cnblogs.com/MouHaoHao/p/10698777.html#mulu)

[PyQtdeploy-V2.4 User Guide 中文 （二）](https://www.cnblogs.com/MouHaoHao/p/10699225.html)