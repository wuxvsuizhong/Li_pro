#python机遇其全局解释器锁GIL的原因(某一时刻只能有单个线程占用CPU)，其实并不能实现真正的多线程，使用python+c能够实现真正的多线程

'''
import threading
#python中使用多线程并不能实现多核并用
#用htop命令查看可以看到两个cpu的占用各50%左右
def work():
	while True:#死循环，会导致CPU空转，占用效率高达100%
		pass



t1 = threading.Thread(target = work)
t2 = threading.Thread(target = work)

t1.start()
t2.start()
'''

'''

#python中使用多进程能够实现真正的多核并用
#htop查看两个cpu都占用100%的
import multiprocessing

def work2():
	while True:
		pass

p1 = multiprocessing.Process(target = work2)
p2 = multiprocessing.Process(target = work2)

p1.start()
p2.start()
'''

#python + c实现多线程多核并用(真正的多线程)
from ctypes  import *
import threading

lib = cdll.LoadLibrary("./libdeadloop.so")#加载c动态库


t1 = threading.Thread(target = lib.DeadLoop) #参数target指定动态库中的函数名字
t1.start()#调用c的死循环函数实现一个死循环线程

while True: #主线程空转
	pass
