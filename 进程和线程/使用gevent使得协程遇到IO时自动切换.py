import time
from gevent import spawn
from gevent import monkey
monkey.patch_all()  #需要给gevent大打上monkey补丁，这样就可以用gevent监控IO操作

#模拟IO密集型任务

def f1():
    for i in range(3):
        print("哒")
        time.sleep(2)

def f2():
    for i in range(3):
        print("咩")
        time.sleep(2)

#单线程下执行IO密集型任务消耗的时间
start = time.time()
f1()
f2()
end = time.time()
print(end-start)   # 两个任务，每个任务循环3次，每次睡眠2秒 ，总时间为 2*3 + 2*3 = 12s
#实际的时间 12.034195184707642


def buyao():
    for i in range(3):
        print("不要")
        time.sleep(3)

# 检测IO操作
start = time.time()
g1 = spawn(f1)  #spawn传入任务函数名，spawn检测是异步提交的
g2 = spawn(f2)
g3 = spawn(buyao)

g1.join()
g2.join()  #需要添加join否则会因为主线程退出而导致任务提前结束
g3.join()

end = time.time()
print(end-start)  # 两个任务，因为添加了IO检测的异步切换操作，使得整个运行的时间大大缩短，约为9s，
# 也就是任务中耗时最长的那个任务的时间，而不是任务串行时所有IO耗时的叠加时长
# 实际运行时间 9.015952825546265