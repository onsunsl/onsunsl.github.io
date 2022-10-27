class UrlGenerator(object):
    def __init__(self, root_url):
        self.url = root_url

    def __getattr__(self, item):
        if item == 'get' or item == 'post':
            print(self.url)
        return UrlGenerator('{}/{}'.format(self.url, item))


url_gen = UrlGenerator('http://xxxx')
url_gen.users.show.get


# 输出http://xxxx/users/show


class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        print(f"__getattr__ 字典key={name}访问")
        value = self[name]
        if isinstance(value, dict):
            value = ObjectDict(value)
        return value


if __name__ == '__main__':
    od = ObjectDict(asf={'a': 1}, d=True)
    print(od.asf, od.asf.a)  # {'a': 1} 1
    print(od.d)
