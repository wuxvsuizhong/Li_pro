import time
from multiprocessing import Process

def func(name):
    print(f"{name}还存活")
    time.sleep(10)
    print(f"{name}退出")


if "__main__" == __name__:
    p = Process(target=func,kwargs={"name":"子进程1"})
    p.daemon = True   #设置子进程为父进程的守护进程之后，当父进程运行完后，会直接终止子进程而不等子进程运行完毕
    p.start()
    print("主进程开始...")
    time.sleep(2)
    print("主进程运行完毕")

