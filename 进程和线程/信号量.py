import random
import time
from threading import Thread,Semaphore

# 信号量用于控制访问特定资源的线程数量，通常用于某些资源有明确访问数量限制额场景，简单说就是用于限流

# 停车场
# 设置车位资源数为5
sp = Semaphore(5)


def task(name):
    sp.acquire()
    print(f"{name}抢到了车位")
    time.sleep(random.randint(3,5))
    sp.release()
    print(f"{name}开走了")

if "__main__" == __name__:
    for i in range(10):
        t = Thread(target=task,args=(f"宝马{i}",))
        t.start()