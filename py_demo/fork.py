import os
import time

ret = os.fork()
if ret == 0:
	'''
	while True:
		print("-----1-----")
		time.sleep(1)
	'''
	print("child,ret=%d"%ret)
	print('getpid=%d'%os.getpid())
else:
	'''
	while True:
		print('-----2-----')
		time.sleep(1)
	'''
	print('parent,ret = %d'%ret)
	print('getpid=%d'%os.getpid())

print("outside")
