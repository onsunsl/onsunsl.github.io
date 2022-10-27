
class ThemeImpl:

    a = "123"
    b = "234"

    def __init__(self):
        self.c = 123412432

    def __getattr__(self, item):
        print(f"找不到`{item}`属性时候才调用__getattr__")
        print("这里可以抛异常")
        return None

    def __getattribute__(self, item):
        print(f'访问`{item}`属性优先调用__getattribute__')
        return super(ThemeImpl, self).__getattribute__(item)


b = ThemeImpl()
print(b.a)
print(b.c)
print(b.d)



