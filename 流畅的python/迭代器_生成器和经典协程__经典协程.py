# #################
# 使用协程计算累计平均值
# #################
from collections.abc import Generator

def average()->Generator[float,float,None]:
    total = 0.0
    count = 0.0
    average = 0.0
    while True:
        term = yield average    # 这里term接收send发送来的值
        total += term
        count += 1
        average = total/count

if __name__ == "__main__":
    coro_avg = average()
    print(next(coro_avg))   # 0.0   # 开始执行协程，使其运送到yield语句,或者通过coro_avg.send(None)也可以促使协程运行到yield处
    # 下面send传送的值，均被average中的term接收
    print(coro_avg.send(10))    # 10.0
    print(coro_avg.send(30))    # 20.0
    print(coro_avg.send(5))     # 15.0

    coro_avg.close()    # 调用close()方法停止协程
    # print(coro_avg.send(20))    # 协程停止后，无法在向协程中发送数据，会报错StopIteration8

# #############
# 让协程返回一个值
# #############
from collections.abc import Generator
from typing import Union,NamedTuple
class Result(NamedTuple):
    count: int
    average:float

class Sentinel:
    def __repr__(self):
        return f'<Sebtinel>'

STOP = Sentinel()
SendType = Union[float,Sentinel]

def average2(verbose:bool = False) ->Generator[None,SendType,Result]:
    total = 0.0
    count = 0.0
    average = 0.0
    while True:
        term = yield
        if verbose:
            print('received:',term)
        if isinstance(term,Sentinel):   # 如果接收到的是Sentinel哨符那么退出while循环，从而结束迭代
            break
        total += term
        count+=1
        average = total/count
    return Result(count,average)

if __name__ == "__main__":
    coro_avg2 = average2()
    next(coro_avg2)
    print(coro_avg2.send(10))   # None
    print(coro_avg2.send(30))   # None
    print(coro_avg2.send(6.5))  # None
    try:
        coro_avg2.send(STOP)
    except StopIteration as exc:
        print(exc.value)    # Result(count=3.0, average=15.5)
# 值得注意的是，average2的迭代最终返回的数据是放在一个Result具名元组对象中的，而且这个最后的结果是作为StopIteration异常的value来传递的
# 这种从StopIteration中获取返回值的方式，不是很好，改用yield from来接收

def compute():
    res = yield from average2(True) # 最终average2的最终的return的结果会被res接收
    print('computed:',res)
    return res

if __name__ == "__main__":
    print('-'*10,"接收协程的返回值",'-'*10)
    comp = compute()
    for v in [None,10,20,30,STOP]:
        try:
            comp.send(v)
        except StopIteration as e:
            result2 = e.value
    # received: 10
    # received: 20
    # received: 30
    # received: <Sebtinel>
    # computed: Result(count=3.0, average=20.0)   打印的compute中的res接收的值

    print("->",result2)     # -> Result(count=3.0, average=20.0)

