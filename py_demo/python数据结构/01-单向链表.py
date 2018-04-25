# -*- coding:utf-8 -*-

class Node(object):
	def __init__(self,item):
		self.item = item
		self.next = None
	

class SingleLinkList(object):
	def __init__(self,node=None):
		self._head = node 

	def is_empty(self):
		return self._head == None

	def length(self):
		'''如果头结点为空那么链表就为空'''
		cur_node = self._head
		count = 0
		while cur_node != None:
			count += 1
			cur_node  = cur_node.next

		return count

	def travel(self):
		'''遍历链表'''
		cur_node = self._head
		while cur_node != None:
			print(cur_node.item)
			cur_node = cur_node.next
			
		
	def add(self,item):
		'''
		头部添加元素
		'''
		if self.is_empty():
			self._head = Node(item)
		else:
			cur_Node = Node(item)
			cur_Node.next = self._head
			self._head = cur_Node



	
	def append(self,item):
		'''
		尾部添加元素
		'''
		if self.is_empty():
			self._head = Node(item)
			return

		cur_Node = self._head;
		while cur_Node.next != None:
			cur_Node = cur_Node.next
		cur_Node.next = Node(item)
		


	
	def insert(self,pos,item):
		if pos >= self.length():
			self.append(item)
		elif pos <=0:
			self.add(item)
		else:
			cur_Node = self._head
			front = None
			for i in range(pos):
				front = cur_Node
				cur_Node = cur_Node.next
			new_Node = Node(item)
			new_Node.next = cur_Node
			front.next = new_Node


	def remove(self,item):
		if self.is_empty():
			return None
		cur_Node = self._head
		front = self._head
		while cur_Node != None:
			if cur_Node.item == item:
				if front == self._head:
					print('found item')
					self._head = front.next
				else:
					front.next = cur_Node.next
				return True
			else:
				front = cur_Node
				cur_Node = front.next
		return False
			

	def research(self,item):
		if self.is_empty():
			return None
		else:
			cur_Node = self._head
			while cur_Node != None:
				if cur_Node.item == item:
					return cur_Node
				else:
					cur_Node = cur_Node.next
			return cur_Node



if __name__ == '__main__':
	link = SingleLinkList()	
	print(link.is_empty())
	print(link.length())
	
	link.append(1)
	
	link.append(2)
	link.append(3)
	link.append(4)
	link.append(5)
	link.append(6)
	link.add(7)
	print(link.is_empty())
	print(link.length())
	print('*'*10)	

	link.insert(2,100)
	link.insert(-3,111)
	link.insert(90,110)

	link.travel()
	
	ret = link.research(1000)
	if ret:
		print(ret.item)
	else:
		print('not found')
	
	ret = link.remove(110)
	if ret:
		print("renove OK")
	else:
		print('not found')
	link.travel()
