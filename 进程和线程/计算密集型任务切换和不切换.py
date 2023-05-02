import time


def f1():
    n = 0
    for i in range(1000000):
        n += i

def f2():
    n = 0
    for i in range(1000000):
        n += 1


start = time.time()
f1()
f2()
end = time.time()
print(end-start)   # 打印运行时间约为 0.0868065357208252

def ff1():
    n = 0
    for i in range(1000000):
        n += i
        yield


def ff2():
    n = 0
    g = ff1()  # 创建ff1的生成器
    for i in range(1000000):
        n += 1
        next(g) # 触发ff1的生成器g执行，从而实现ff1和ff2来回切换运行

start = time.time()
ff1()
ff2()
end = time.time()
print(end-start)   # 打印运行时间约为 0.1312391757965088

# 对比可以看出，在计算密集型的任务中，任务切换反而导致了运行时间的增长




