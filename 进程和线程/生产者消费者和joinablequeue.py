import random
import time
from multiprocessing import Process,Queue,JoinableQueue

# JoinableQueue和Queue几乎相同，区别是它实现了一个消息计数，添加消息的时候计数加1，等队列中的消息消费完毕后，计数会减小到0
# JoinableQueue的join方法会一直阻塞等到计数减小到0

def producer(name,food,q:JoinableQueue):
    for i in range(10):
        time.sleep(random.randint(1,3))
        print(f"{name}生产了{food}{i}")
        q.put(f"{food}{i}")

def consumer(name,q):
    while True:
        food = q.get()
        print(f"{name}吃了{food}")
        time.sleep(random.randint(1,5))
        q.task_done()   #每调用一次，JoinableQueue的计数减小1


if "__main__" == __name__:
    q = JoinableQueue()
    p1 = Process(target=producer,kwargs={"name":"厨师1","food":"蛋炒饭","q":q})
    p2= Process(target=producer,kwargs={"name":"厨师2","food":"炸酱面","q":q})

    c1 = Process(target=consumer,kwargs={"name":"八戒","q":q})
    c2 = Process(target=consumer,kwargs={"name":"唐僧","q":q})

    p1.daemon = True
    p2.daemon = True
    c1.daemon = True
    c2.daemon = True
    # 设置子进程的守护进程标志，当主进程监控到所有子进程任务结束后，子进程跟主进程结束

    p1.start()
    p2.start()
    c1.start()
    c2.start()

    p1.join()
    p2.join()
    # 保证生产者生产完毕


    q.join()    #当JoinableQueue中的消息被消费完后，JoinableQueue等待计数减小到0
    print("队列空")
