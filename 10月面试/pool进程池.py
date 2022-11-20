#进程池中每个进程打印从0-n的数字
from multiprocessing import Pool
import os,time


def work(n,index):
    for i in range(n):
        print("in process {}, index is {}, ---{}---".format(os.getpid(),index,i))
        time.sleep(2)
    return


def main():
    po = Pool(5)
    for index in range(10):
        #10个任务，依次发送到进程池中
        print("add {} to pool...".format(index))
        po.apply_async(work,args=(5,index))
        # po.apply(work,args=(5,index))

    print("-----start-----")

    #关闭进程池后，进程池不再接受新任务
    po.close()
    #join必须在close之后
    #join等地所有进程结束
    po.join()

    print("-----end-----")

if __name__ == '__main__':
    main()
