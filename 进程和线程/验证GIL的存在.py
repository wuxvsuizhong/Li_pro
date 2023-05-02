import time
from threading import Thread,Lock

num = 100
mutex = Lock()


def work():
    global num
    # mutex.acquire()
    temp = num
    # time.sleep(0.001)  #加了IO延时后，GIL会释放，这就不能保证原子操作了
    num = temp - 1
    # mutex.release()


if "__main__" == __name__:
    ths = []
    for i in range(num):
        th = Thread(target=work)
        ths.append(th)
        th.start()

    for t in ths:
        t.join()

    print(num)  #如果多线程的任务中没有IO中断释放GIL锁，即便在不加互斥锁的情况下，最终num的值也能正常的减小到0
    # 因为GIL存在，在一个进程内,某个时刻只有一个线程获取到GIL并运行程序，所以也能避免了全局访问冲突的问题，
    # 但是有一个前提：GIL会在等待IO时释放锁，这就导致额一个现象，如果在修改全局变量的时候，有了IO操作比如sleep,那么线程会把GIL交出去，给其他的线程。
    # 而线程之前获取到全局变量比如num = 100,在下一次获取到GIL锁之后还会按照之前的变量值去运算，这在多线程的时候又会导致修改混乱
    # 所以如果要想不混乱，那么在访问全局变量的时候不要额外的IO操作，让获取和修改变量编程一个原子操作即可，也就是保证GIL不会被释放
    # 但是通常会添加互斥Lock来多一道保障，在程序员层面还是不依赖GIL锁来保证数据安全，尽管GIL锁也可以实现锁保证数据安全
