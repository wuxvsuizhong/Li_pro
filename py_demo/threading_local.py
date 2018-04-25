import threading

localschool = threading.local()

def work1():
	std = localschool.student
	print('Hello,%s in %s'%(std,threading.current_thread().name))

def work2(name):
	localschool.student = name
	work1()


t1 = threading.Thread(target = work2,args = ('T1',),name = 'thread1')
t2 = threading.Thread(target = work2,args = ('T2',),name = 'thread2')

t1.start()
t2.start()

t1.join()
t2.join()
