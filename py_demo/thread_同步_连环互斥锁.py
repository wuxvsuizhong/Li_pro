from threading import Thread,Lock
from time import sleep


class Task1(Thread):
	def run(self):
		while True:
			if lock1.acquire():
				print("-----task1-----")
				sleep(1)
				lock2.release()

class Task2(Thread):
	def run(self):
		while True:
			if lock2.acquire():
				print('-----tesk2-----')
				sleep(1)
				lock3.release()

class Task3(Thread):
	def run(self):
		while True:
			if lock3.acquire():
				print('-----task3-----')
				sleep(1)
				lock1.release()


lock1 = Lock()
lock2 = Lock()
lock2.acquire()
lock3 = Lock()
lock3.acquire()

t1 = Task1()
t2 = Task2()
t3 = Task3()
t1.start()
t2.start()
t3.start()
				
				
				
