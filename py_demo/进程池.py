from multiprocessing import Pool
import time
import os

def func(num):
	for i in range(num):
		print('-----1-----%d,pid = %d'%(i,os.getpid()))
		time.sleep(1)



po = Pool(5)
for i in range(10):
	print('add %d'%i)
	po.apply_async(func,(i,))
po.close()
po.join()
