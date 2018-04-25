# -*- coding:utf-8 -*-


class Stack(object):
	def __init__(self):
		self.__list = []
	
	def push(self,item):
		self.__list.append(item)
	
	def pop(self):
		if not self.is_empty():
			return self.__list.pop()
		else:
			return None
	
	def peek(self):
		'''返回栈顶元素'''
		if self.__list:
			return self.__list[-1]
		else:
			return None
	
	def is_empty(self):
		return self.__list == []
	
	def size(self):
		return len(self.__list)

		
if __name__ == '__main__':
	s = Stack()
	print(s.size())
	s.push(1)
	s.push(2)
	s.push(3)
	s.push(4)
	s.push(5)
	
	print(s.pop())
	print(s.pop())
	print(s.pop())
	print('*'*10)
	print(s.peek())
	print(s.pop())
	print(s.pop())
	print(s.pop())
