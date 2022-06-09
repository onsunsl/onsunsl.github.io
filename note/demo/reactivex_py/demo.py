from reactivex import of
from reactivex import operators as op

data = [1, 23, "str"]

# 生成一个可观察对象Observable[_T]
ob1 = of(*data)
ob1.subscribe(on_next=lambda n: print(f"next:{n}"))

ob2 = of(1, 2, 34, 5, 6, 7, 7)
ob2new = ob2.pipe(op.map(lambda i: i ** 2), op.filter(lambda i: i >= 10))
ob2new.subscribe(lambda i: print(f'Received: {i}'))
