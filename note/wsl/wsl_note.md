WSL 是windows 下的linux 子系统， 可以同时运行windows和ubuntu linux. 文件可以互相访问
非常方便。WSL 是windows 与linux 交互的桥梁，类似虚拟机，所以需要安装WSL再安装linux系统。

win10 下的Microsoft Store 被我弄坏了，怎么都修复不了，直接升级到win11,然后安装ubuntu. 终于可以使用了

为了节省系统资源我在Microsoft Store 里安装了ubuntu18.04版本

18.04 里面自带了python3.6 版本，没有python 和python2, 连pip也没有, 使用apt 安装一下
```shell
lin@BJ-PF2WYZBP:~$ sudo apt install python3-pip
[sudo] password for lin:
Reading package lists... Done
Building dependency tree
Reading state information... Done
E: Unable to locate package python3-pip
```
apt 软件库里找不到， 估计是source list 有问题了， 更新一下

> sudo apt update



ubuntu2004.exe config --default-user root




参考:

[WSL备份与还原（使用Win10自带工具）](https://blog.csdn.net/code_peak/article/details/118769378)

[修改WSL默认默认用户](https://www.cnblogs.com/Hiro666/p/14119763.html)