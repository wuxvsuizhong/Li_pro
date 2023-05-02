import random
import time
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(10)


def task(name):
    print(f"{name}")
    time.sleep(random.randint(3,5))

    return f"{name}完成"

def get_res(res):
    print(res.result())



if "__main__" == __name__:
    l = []
    for i in range(50):
        future = pool.submit(task,f"任务{i}")
        # print(future.result())
        #如果在提交完任务后直接获取线程池中任务的结果，那么会阻塞等待结果，
        # 直到有结果返回，才会继续往下执行，这时就从异步变成了同步

        l.append(future)  #提交完任务后先把结果对象放置在列表中，这样就不会阻塞等待结果了

    # 方式1
    # 异步获取线程池总提交任务的返回值
    # 先添加任务，在获取异步提交的任务的结果
    for each in l:
        print(each.result())

    # 方式2
    # 如果是需要等待所有的提交的任务都先执行完毕后，在同一获取结果
    # pool.shutdown() #或阻塞等待线程池中所有的任务都提交并且运行完毕才会往下走
    # for each in l:
    #     print(each.result())

    # 方式3——推荐
    # 添加回调函数，在异步提交任务后，由线程池自动调用回调函数获取任务结果
    for i in range(50):
        # 异步提交任务时添加回调函数获取任务结果
        pool.submit(task,f"————任务{i}————").add_done_callback(get_res)
