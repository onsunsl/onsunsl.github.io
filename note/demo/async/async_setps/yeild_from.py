def gen():
    r = yield from subgen()
    r += 3
    print(f"gen:{r}")
    return r

def subgen():
    while True:
        x = yield
        print(f"subgen:{x}")
        yield x+1

def main():
    g = gen()
    print(f"gen type:{g}")
    next(g)                # 驱动生成器g开始执行到第一个 yield
    retval = g.send(1)     # 看似向生成器 gen() 发送数据
    print(retval)          # 返回2
    print(g.send(10))
    # g.throw(StopIteration) # 看似向gen()抛入异常

main()