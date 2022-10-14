import functools
import logging

codes = '''
def fun(a, *args, **kwargs):
     return a+1
'''


def exec_str_fun(code: str, *args, **kwargs):
    """
    运行函数
    """
    try:
        namespace = {}
        fun = compile(code, '<string>', 'exec')
        exec(fun, namespace)
        return namespace['fun'](*args, **kwargs)
    except Exception as err:
        logging.error(f"exec:{code} error: {err}", exc_info=True)
        return None


print(exec_str_fun(codes, 1))
# ------------------------------

# 字符串转python 对象
print(eval("dict(a=234)"))

# 通过字符串取python 对象
d = dict(a=234)
print(eval('d["a"]', globals()))


def demo2(a=234):
    c = dict(a=345435)
    # 取全局对象
    print(eval('d["a"]', globals(), locals()))

    # 取局部对象
    print(eval('c["a"]', globals(), locals()))

    # 取局部对象
    print(eval('a', globals(), locals()))


demo2()

eval2 = functools.partial(eval, globals(), locals())


def exec(code, local=None):
    return eval(code, globals(), local)


print("====================")


def demo3(a=234):
    c = dict(a=345435)
    print(exec('d["a"]'), locals())
    print(exec('c["a"]'))
    print(exec('a'))


demo3()
