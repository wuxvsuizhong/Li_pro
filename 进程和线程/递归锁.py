import time
from threading import Thread,RLock,current_thread
# 递归锁Rlock实际是一种带有计数器的互斥锁，没获取一次递归哦就会把计数器加1
# 只有递归锁的计数减小到0的时候才会释放，然后由其他的线程或者进程来获取锁

num = 100
mutex = RLock()
mutex2 = mutex
# mutex和mute2实际是同一个锁对象  

def task2():
    mutex2.acquire()
    print(current_thread().name,"抢到锁")
    time.sleep(1)
    mutex.acquire()
    print(current_thread().name,"抢到锁")
    mutex.release()
    mutex2.release()

def task1():
    mutex.acquire()
    print(current_thread().name,"抢到锁")
    mutex2.acquire()
    print(current_thread().name,"抢到锁2")
    mutex.release()
    mutex2.release()
    task2()


if "__main__" == __name__:
    for i in range(8):
        t = Thread(target=task1)
        t.start()
