## windows server 搭建pypiServer 

在团队内部场景私有的pypi仓


### 安装
`pip install pypiserver` 


### 启动服务
创建一个pypi server 的启动脚本 `pypi_server_start.bat`， 内容如下
```shell
.\Scripts\pypi-server.exe run -p 9090 -P . -a . --log-file .\log\pypi_server.log --fallback-url https://pypi.doubanio.com/simple  D:\ftp\pypi_packages -v -o
```

* `pypi-server.exe` 是安装pypiServer后在python 安装目录下生成的
* `run` 启动服务
* `-p 9090` 服务端口
* `-P .` 密码文件为空， 即无用户、密码验证
* `-a .` 无权限校验，即update|download|list都有权限
* `--log-file .\log\pypi_server.log`  日志文件
* `--fallback-url https://pypi.doubanio.com/simple` 当私仓内包不存在时候到`douban`仓查找
* `D:\ftp\pypi_packages` pypi 仓的跟目录
* `-v` 在console 展示日志
* `-o` 覆盖已存在的包

启动成功后可以在浏览器里访问

![](static\images\pypi_server.png)



### 测试安装一个公网包

测试安装一个公网`pyserial`包, 并把安装源指向自己搭建的私仓`pip install pyserial -i http://your_ip:your_port/simple`
```shell
Looking in indexes: http://your_ip:your_port/simple
WARNING: The repository located at 10.248.224.41 is not a trusted or secure host and is being ignored. If this repository is available via HTTPS we recommend you use HTTPS instead, otherwise you may silence this warning and allow it anyway with '--trusted-host 10.248.224.41'.
ERROR: Could not find a version that satisfies the requirement pyserial (from versions: none)
ERROR: No matching distribution found for pyserial
WARNING: You are using pip version 21.1.2; however, version 21.3.1 is available.
You should consider upgrading via the 'C:\Users\xxxxx\pythonEnv\withPdbInfo\Scripts\python.exe -m pip install --upgrade pip' command.
```

发现pip报错了，需要https访问， 解决办法：
* 把自己搭建pipy server私仓改成https服务
* pip 安装时候添加`--trusted-host you_ip`

使用方法2再次安装， 成功了，而且包是从`douban`的源里下载的
`pip install pyserial -i http://your_ip:your_port/simple --trusted-host your_ip`

```shell
Looking in indexes: http://your_ip:your_port/simple
Collecting pyserial
  Using cached https://pypi.doubanio.com/packages/07/bc/587a445451b253b285629263eb51c2d8e9bcea4fc97826266d186f96f558/pyserial-3.5-py2.py3-none-any.whl (90 kB)
Installing collected packages: pyserial
Successfully installed pyserial-3.5

```

### 上传第一个包
#### 创建一个简单的包
first_package/__init__.py
```python

def hello():
    print("hello, this is my  first pypi server package!")
```

setup.py
```python
from setuptools import setup

setup(
    name="first_package",
    version="0.0.1",
    description="Test my pypi server",
    author="Onunsl",
    author_email="Onsunsl@foxmail.com",
    url="https://www.jili.ink",
    packages=["first_package"],
)
```
打包.whl包`python setup.py bdist_wheel` 输出到dist目录，这里需要python环境已经安装了setuptools 和 wheel 包，


#### 上传到私仓
据说setuptools里的upload命令有安全隐患，所以推荐使用twine工具，所以需要安装它`pip install twine`, 随后上传
`twine upload --repository-url http://ip:port/ dist/*`
```shell
Uploading distributions to http://ip:port/
Enter your username:
  Your username is empty. Did you enter it correctly?
  See https://twine.readthedocs.io/#entering-credentials for more information.
Enter your password:
  Your password is empty. Did you enter it correctly?
  See https://twine.readthedocs.io/#entering-credentials for more information.
Uploading first_package-0.0.1-py3-none-any.whl
  0%| 
```

过程中提示需要输入密码， enter键跳过即可

### 测试安装私仓内的包

`pip install first_package==0.0.1 -i http://ip:port/  --trusted-host 10.248.224.41`

```shell
Looking in indexes: http://ip:port/
Collecting first_package==0.0.1
Downloading http://ip:port/packages/first_package-0.0.1-py3-none-any.whl (1.5 kB)
Installing collected packages: first-package
Successfully installed first-package-0.0.1
WARNING: You are using pip version 21.1.2; however, version 21.3.1 is available.
You should consider upgrading via the 'C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Scripts\python.exe -m pip install --upgrade pip' command.
```

### 打包&安装拷贝非代码的数据
* 添加MANIFEST.in 文件
* setup() 添加如下选项
```python
    include_package_data=True,
    package_data={
        # 根据你自己的目录决定
        "first_package.data": ["first_package/data/*"]
    }
```


### 依赖包问题
* 依赖包可以在setup.py里调用pip包解析requirements.txt ，然后把结果赋给setup函数的install_requires参数，[参考](https://qastack.cn/programming/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py)
* 如果依赖包在自定义的私仓里，可以在`dependency_links`参数里列优先顺序，把私仓列放在第一位，如：
```python
INDEX_URLS = [
    # your pypi server link
    # "https://pypi.douban.com/simple/"
]
setup(
    # 依赖模块安装源
    dependency_links=INDEX_URLS
)
```

### demo 源码
[first_package](./setup.py)


### 参考
* [pypiserver](https://pypi.org/project/pypiserver/)
* [搭建pypiserver私有源](https://blog.csdn.net/qq_45957580/article/details/123185498)
* [使用setuptools对Python进行打包分发](https://zhongneng.github.io/2019/01/19/python-setuptools/)
* [Python打包时添加非代码文件的坑](https://zhuanlan.zhihu.com/p/24312755)