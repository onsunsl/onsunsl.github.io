国内访问github特别慢， 主要是DNS域名解析的问题：

解决方式：

* 获取最快的github [IP与host列表文件](https://raw.hellogithub.com/hosts)
* 以理员身份用编辑器打开`C:\Windows\System32\drivers\etc\hosts`, 复制ip解析到host文件内保持
* CMD 窗口输入 `ipconfig /flushdns` 刷新域名解析