from multiprocessing import Process
import time
import os

class MyProcess(Process):
	def __init__(self):
		Process.__init__(self)
	
	def run(self):
		print('child %d start,parent is %d'%(os.getpid(),os.getppid()))
		while True:
			print('-----1-----')
			time.sleep(1)

p = MyProcess()
p.start()

while True:
	print('-----main-----')
	time.sleep(1)
