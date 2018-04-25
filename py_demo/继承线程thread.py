import threading
import time

class MyThread(threading.Thread):
	def run(self):
		for i in range(5):
			time.sleep(1)
			msg = "I'm" + self.name + '@' + str(i)#name属性是python给线程分配的名称
			print(msg)




if __name__ == '__main__':
	for i in range(3):
		t = MyThread()
		t.start()
