def gen():
    print("step2")
    r = yield from subgen()
    r += 3
    print(f"step7:{r}")
    return r


def subgen():
    print(f"step3")
    x = yield
    print(f"step5:{x}")
    yield x+1
    return x


def main():
    print("step1")
    g = gen()
    print(f"gen type:{g}")
    next(g)                     # 驱动生成器g开始执行到第一个 yield
    print("step4")
    result = g.send(1)          # 看似向生成器 gen() 发送数据
    print("step6", result)      # 返回2
    print("step8", g.send(10))
    # g.throw(StopIteration)    # 看似向gen()抛入异常

main()

