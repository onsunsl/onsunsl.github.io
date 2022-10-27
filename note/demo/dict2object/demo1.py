"""
这实现了任意字典转对象的功能， 无需对类成员变量预设
同样的方法还可以python3.7 以后的dataclass和三房库pydantic， 而这两种的成员变量都是预设（固定的）
"""
from collections import UserDict


class Dict2Object(UserDict):

    dd = dict(d=11, b=22, c=dict(aa=555))

    def __getitem__(self, item):
        print(f"get {item}")
        if item in self.data:
            return self.data[item]
        else:
            return self.dd[item]

    # 这里self.data 会触发__getattr__ 的递归调用
    # def __setitem__(self, key, value):
    #     # print(f"set {key}, {value}")
    #     self.data[key] = value

    # __setattr__ = dict.__setitem__
    __getattr__ = __getitem__


class Dict2Object2(dict):

    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict2object(dict_obj):
    if isinstance(dict_obj, list):
        instance_list = []
        for i in dict_obj:
            instance_list.append(dict2object(i))
        return instance_list

    if not isinstance(dict_obj, dict):
        return dict_obj
    instance = Dict2Object()
    for k, v in dict_obj.items():
        instance[k] = dict2object(v)
    return instance


o = dict2object(dict(a=1, b=2, c=dict(aa=123)))
print(o.a)
print(o.c.aa)
print(o.d)
