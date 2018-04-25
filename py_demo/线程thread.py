from threading import Thread
import time

def test():
	print('--------1--------')
	time.sleep(1)

for i in range(5):
	t = Thread(target = test)
	t.start()
