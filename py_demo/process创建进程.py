from multiprocessing import Process
import time

def func():
	for i in range(5):
		print('------test------')
		time.sleep(1)
	
p = Process(target = func)
p.start()

'''
while True:
	print("-----main-----")
	time.sleep(1)
'''
p.join(2)
print('----main----')
p.terminate()
