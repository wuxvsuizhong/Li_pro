# -*- coding:utf-8 -*-


class Queue(object):
	def __init__(self):
		self.__list = []
	
	def enqueue(self,item):
		self.__list.insert(0,item)
		'''入队'''
	
	def dequeue(self):
		'''出队'''
		if not self.is_empty():
			return self.__list.pop()
		else:
			return None
	
	def is_empty(self):
		return self.__list == []
	
	def size(self):
		return len(self.__list)






if __name__ == '__main__':
	q = Queue()
	q.enqueue(1)
	q.enqueue(2)
	q.enqueue(3)
	q.enqueue(4)
	q.enqueue(5)

	print(q.dequeue())
	print(q.dequeue())
