### 依赖注入

`依赖注入`是解决一个对象如何获得它依赖的其他对象的解耦技术

> 例如: A 依赖 B和C

那一个对象A可以通过`注入器(Injector)`获得它所依赖的其他对象B、C。
其中B、C对象是A对象的依赖(Dependencies)被`传入`到A对象中，B和C一般被称为`Service`服务，A作为接收对象一般叫`Client`客户端，
而负责将依赖传递入接收对象的代码叫做`Injector`注入器。

因此我们可以看到Client具体使用什么Service是由Injector去指定的，并传入到Client中，而不是Client自己去指定或创建的，
这一点也是依赖注入的基本要求。

`依赖注入`是控制反转(Inversion of Control)这种技术的一种形式。目的是为了进一步解耦对象。Client需要某种服务，
但是它仅仅知道这种服务(接口），而不知道具体实现服务的是哪个类。Client把找到这个实现类的工作交给Injector去完成。
Injector会把找到的实现类的实例通过Client提供的注入方式注入到Client中。这样一来Client就和具体的服务实现解耦了，
Client既无需要知道具体的服务实现，也能使用到服务了。

依赖注入将Client的依赖的创建和Client本般的行为分割开来。依赖注入促进了松耦合编程、依赖反转、单一责任原则等这些编程设计思想。

依赖注入这种技术中，一般包含四种角色，各司其职：
* Service 对象，它包含了Client要使用的服务。
* interface接口，通过它Client只知道有什么服务，而不需要知道具体实现。
* Client对象，它的行为依赖于它所使用的服务
* Injector注入器，它负责构造具体的Service并将其传入到Client对象中。


Client通过以下方式(不限于)来向Injector提供注入口：

* 构造器注入，即通过Client的构造器注入，简单来说就是new这个Client对象时，通过它的构造函数把依赖传进去。
* set方法注入，即Client对象提供一些set方法，Injector就可以调用set方法把依赖传进去。
* 接口注入，即这些依赖的接口提供一个注入器方法



python 下的DI 框架 dependency-injector

参考
[dependency-injector](https://python-dependency-injector.ets-labs.org/)
[再聊：依赖注入（Dependency injection）](https://blog.csdn.net/weixin_40763897/article/details/122448500)

