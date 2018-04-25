from threading import Thread,Lock
import time

g_num = 0

def work1():
	global g_num
	for i in range(1000000):
		mutex.acquire()
		g_num += 1
		mutex.release()
	print('---work1---,g_num = %d'%g_num)

def work2():
	global g_num
	for i in range(1000000):
		mutex.acquire()
		g_num +=1
		mutex.release()
	print('---work2---,g_num = %d'%g_num)

mutex = Lock()
t1 = Thread(target = work1)
t2 = Thread(target = work2)

t1.start()
t2.start()

