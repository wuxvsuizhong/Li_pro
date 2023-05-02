import random
import time
from threading import Thread

def w1(name):
    print(f"{name}活动")
    time.sleep(2)
    print(f"{name}结束")

def w2(name):
    print(f"{name}活动")
    time.sleep(3)
    print(f"{name}结束")

if "__main__" == __name__:
    th1 = Thread(target=w1,args=("任务1",))
    th2 = Thread(target=w2,args=("任务2",))

    # th2.daemon = True  #虽然w2的运行时间长，但是设置了deamon标志后，会提前跟着主线程运行完毕而结束，所以w2的结束表示不会打印
    th1.daemon = True   #如果设置的是w1的守护线程标志，w1的运行时间短，但是因为主线程会等待其他的运行时间长的线程运行完毕，所以结束标志会正常打印

    # 总结：设置了守护线程的子线程，主线程不会等待其运行结束，反之子线程会跟随主线程的结束
    # 如果设置了守护线程的标志的线程的运行时间是短，那么不会影响其正常结束，因为主线会等待其他时间长的线程的结束
    # 如果设置的守护线程是时间长的线程，那么因为主线程等待的时间短，所以守护线程时间长的会提前终止

    th1.start()
    th2.start()

    print("主线程")