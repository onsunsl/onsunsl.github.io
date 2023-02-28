### wsl 安装之后无法连接正常解析域名

#### 问题
```log
Err:4 http://archive.ubuntu.com/ubuntu bionic-backports InRelease
  Temporary failure resolving 'archive.ubuntu.com'
```

#### 解决
修改`sudo vim /etc/resolv.conf`内容为： 

```log
[network]
generateResolvConf = false
nameserver 223.6.6.6
```
