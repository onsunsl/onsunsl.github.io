c = 123
def f1():
    a = 1
    b = 2
    def f2(d):
        print(a, b, c, d)
    return f2
fun2 = f1()
fun2(c)

# 但这里调用的是f1的字节码
print(f1.__code__.co_cellvars)  # ('a',)