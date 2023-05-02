import random
import time
from threading import Thread,Event

# Event可以用于在线程之间传递事件，相当于一个信号，
# 某个事件发出以后，一些等待Event事件的编程就可以继续运行了，否则一直等待

# 乘客等公交车事件

event = Event()

def bus():
    print("公交车即将到站")
    time.sleep(random.randint(3,5))
    print("公交车到站")
    # t通知乘客线程上车
    event.set()  #发送信号，车来了快上车

def passenger(name):
    print(f"{name}正在等车...")
    event.wait()  #阻塞等待event信号，一旦event发出了信号，就往下执行
    print(f"{name}上车了")

if "__main__" == __name__:
    b = Thread(target=bus)
    b.start()

    for i in range(10):
        p = Thread(target=passenger,args=(f"乘客{i}",))
        p.start()
