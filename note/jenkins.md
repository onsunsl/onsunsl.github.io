## Jenkins 

Jenkins 会为每job 保存，所以Home目录需要有足够空间，否则后期迁移可能会导致重新配置

### 修改Home目录
参考了[Jenkins修改workspace和build目录 ](https://www.cnblogs.com/itech/p/5192162.html) 发现我使用的版本没有`高级`的按钮
然后修改JENKINS_HOME， 但是也么有生效，参考了[修改JENKINS_HOME](https://www.cnblogs.com/WilsonX/p/6640148.html)

> 注意: 修改之前需要把原理的数据迁移到新的目录下

步骤：
* 环境变量里设置`JENKINS_HOME` 指向新的目录
* 搜索`jenkins.xml` 配置文件， 并备份原来的文件；
* 按照[修改JENKINS_HOME](https://www.cnblogs.com/WilsonX/p/6640148.html) 修改
* 把原来的数据拷贝到新的目录，如： `C:\Users\Administrator\AppData\Local\Jenkins` 拷贝到 `C:JenkinsHome\Jenkins`
* 重启服务，httP://localhost:8080/restart
* 保留原来的`\Jenkins\war` 内容，如果一切正常后删除`Jenkins\.jenkins` 这些包含了过去构建时候产生的数据和插件什么的