from queue import Queue
#python3用小写queue模块
#python2用大写的Queue模块
from threading import Thread
from time import sleep

class producer(Thread):
	def run(self):
		global queue
		count = 0
		while True:
			if queue.qsize() < 1000:
				for i in range(10):
					count += 1
					msg = '生成产品'+str(count)
					queue.put(msg)
					print(msg)
			sleep(0.5)

class consumer(Thread):
	def run(self):
		global queue
		while True:
			if queue.qsize() > 100:
				msg = '消耗'+queue.get()
				print(msg)
			sleep(0.5)


if __name__ == '__main__':
	queue = Queue()

	for i in range(500):
		queue.put('初始产品'+str(i))
	for i in range(3):
		p = producer()
		p.start()
	for i in range(5):
		p = consumer()
		p.start()

