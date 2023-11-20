# 对一个小型数据集做素数检测

# #####################
# 顺序检测
# #####################
import math
from time import perf_counter
from typing import NamedTuple

def is_prime(n:int)->bool:
    """一个检测素数的函数"""
    if n<2:
        return False
    if n == 2:
        return True
    if n%2 == 0:    # 如果是大于2的偶数，那么可以直接判定不是素数
        return False

    root = math.isqrt(n)    # 对n开平方
    for i in range(3,root+1,2): # 只提取检测3~root+1 之间的各个奇数项作为除数
        if n % i == 0:
            return False
    return True

NUMBERS = [
    2,142702110479723,299593572317531,3333333333333301,3333333333333333,3333335652092209,
    4444444444444423,4444444444444444,4444444488888889,5555553133149889,2222222222222203,
    5555555555555555,6666666666666666,6666666666666719,6666667141414921,7777777536340681,
    7777777777777753,7777777777777777,9999999999999917,9999999999999999
]

class Result(NamedTuple):
    prime: bool
    elapsed: float

def check(n: int)->Result:
    t0 = perf_counter()
    prime = is_prime(n)
    return Result(prime,perf_counter()-t0)

def main1()->None:
    print(f'顺序检查{len(NUMBERS)} 个数字:')
    t0 = perf_counter()
    for n in NUMBERS:
        prime,elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16} {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0
    print(f'共计消耗时长:{elapsed:.2f}s')

# if __name__ == "__main__":
#     main1()

# #####################
# 多进程检测
# #####################
import sys
from multiprocessing import Process,SimpleQueue,cpu_count,queues

class PrimeResult(NamedTuple):
    n:int
    prime:bool
    elapsed:float

# 创建类型别名JobQueue和ResultQueue
JobQueue = queues.SimpleQueue[int]
ResultQueue = queues.SimpleQueue[PrimeResult]

def check(n:int)->bool:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n,res,perf_counter() - t0)

def worker(jobs:JobQueue,results:ResultQueue) ->None:
    """从jobs队列中获取一个个的待处理数据，当获取的数据是哨兵数字0时，终止处理"""
    while n := jobs.get():
        results.put(check(n))
    results.put(PrimeResult(0,False,0.0))

def start_jobs(procs:int,jobs:JobQueue,results:ResultQueue)->None:
    for n in NUMBERS:
        jobs.put(n)     # 把待处理的数字NUMBERS项放入jobs队列中
    for _ in range(procs):  # 启动pros数量个进程，并行处理
        proc = Process(target=worker,args=(jobs,results))
        proc.start()
        jobs.put(0) # 往jobs队列中放入哨兵数字，使得子进程能够识别结束标志

def main_procs()->None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'启动{procs}个进程检查{len(NUMBERS)}个数据是否素数:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results:ResultQueue = SimpleQueue()
    start_jobs(procs,jobs,results)
    checked = report(procs,results)
    elapsed = perf_counter() - t0
    print(f'{checked} 检查完成，时间{elapsed}s')

def report(procs:int,results:ResultQueue)->int:
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n,prime,elapsed = results.get()
        if n == 0:
            procs_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')
    return checked

if __name__ == "__main__":
    main_procs()

