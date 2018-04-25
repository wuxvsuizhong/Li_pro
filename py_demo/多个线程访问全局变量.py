import threading
from threading import Thread
from time import sleep

#num = 0

def func():
	num = 0
	while True:
	#	global num
		
		msg = threading.current_thread().name
		print('thread name =%s,num = %d'%(msg,num))
		if msg == 'Thread-1':
			num += 1
			sleep(0.5)
		else:
			sleep(1)



t1 = Thread(target = func)
t2 = Thread(target = func)
t1.start()
t2.start()
