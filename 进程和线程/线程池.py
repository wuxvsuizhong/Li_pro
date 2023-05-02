from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor    #分别是线程池和进程池
import time

pool = ThreadPoolExecutor(10)   #不传参是话，默认线程池中线程的个数就是CPU的核数 * 5 个线程

def task(name):
    print(name)
    time.sleep(2)

for i in range(50):
    pool.submit(task,f"任务{i}")    #线程的默认提交任务方式是异步提交
print("主线程")   #这里不会等待线程池中的子任务执行完毕，主线程会继续运行自己的任务，也就睡主线程和线程池中的任务是异步的

