def timer(func):
    import time
    def wrapper(*args, **kwargs):
        startTime = time.time()
        f = func(*args, **kwargs)
        endTime = time.time()
        passTime = endTime - startTime
        print("执行函数%s使用了%0.2f秒" % (getattr(func, "__name__"), passTime))
        return f

    return wrapper


def do_something(a):
    return a + 1


@timer
def demo1():
    b = 0
    for i in range(1000000):
        b += do_something(i)


@timer
def demo2():
    b = 0
    try:
        for i in range(1000000):
            b += do_something(i)
        raise Exception()
    except Exception as e:
        _ = e
    else:
        pass
    finally:
        pass


@timer
def demo3():
    b = 0
    for i in range(1000000):
        try:
            b += do_something(i)
        except Exception:
            b += do_something(i)
        else:
            pass
        finally:
            pass


@timer
def demo4():
    b = 0
    for i in range(1000000):
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            b += do_something(i)
        else:
            pass
        finally:
            pass


@timer
def demo5():
    b = 0
    for i in range(1000000):
        try:
            raise ZeroDivisionError
        except BaseException:
            b += do_something(i)
        else:
            pass
        finally:
            pass


@timer
def demo6():
    zero = 0
    b = 0
    for i in range(1000000):
        try:
            raise ZeroDivisionError
        except:
            b += do_something(i)
        else:
            pass
        finally:
            pass


@timer
def demo7():
    zero = 0
    b = 0
    try:
        if zero == 0:
            raise ZeroDivisionError
    except ZeroDivisionError:
        for i in range(1000000):
            b += do_something(i)
    else:
        pass
    finally:
        pass


@timer
def demo8():
    zero = 0
    b = 0
    for i in range(1000000):
        if zero == 0:
            b += do_something(i)


demo1()
demo2()
demo3()
demo4()
demo5()
demo6()
demo7()
demo8()

"""
执行函数demo1使用了0.22秒
执行函数demo2使用了0.19秒
执行函数demo3使用了0.20秒
执行函数demo4使用了0.44秒
执行函数demo5使用了0.44秒
执行函数demo6使用了0.39秒
执行函数demo7使用了0.18秒
执行函数demo8使用了0.18秒
"""
