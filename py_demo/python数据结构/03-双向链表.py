# -*- coding:utf-8 -*-

class Node(object):
	def	__init__(self,item=None):
		self.item = item
		self.pre = None
		self.next = None
	

class DoubleDirectionLink(object):
	def __init__(self,node=None):
		self.__head = node
	
	def add(self,item):
		new_node = Node(item)
		if self.is_empty():
			self.__head = new_node
		else:
			new_node.next = self.__head
			self.__head.pre = new_node
			self.__head = new_node


	def append(self,item):
		new_node = Node(item)
		if self.is_empty():
			self.__head = new_node
		else:
			cur_node = self.__head
			while cur_node.next is not None:
				cur_node = cur_node.next
			cur_node.next = new_node
			new_node.pre = cur_node
			
	def insert(self,pos,item):
		if self.is_empty():
			self.add(item)
			return
		elif pos > self.length():
			self.append(item)
			return
		elif pos <=0:
			self.add(item)
			return
		else:
			new_node = Node(item)
			cur_node = self.__head
			for i in range(pos-1):
				cur_node = cur_node.next
			if cur_node.pre is not None:#判断是否只有单个元素
				cur_node.pre.next = new_node
			new_node.pre = cur_node.pre
			new_node.next = cur_node
			cur_node.pre = new_node


	def remove(self,item):
		if self.is_empty():
			return False
		else:
			cur_node = self.__head
			while cur_node is not None:
				if cur_node.item == item:
					if cur_node == self.__head:#删除的元素位于头结点
						self.__head = self.__head.next
						if self.__head is not None:
							self.__head.pre = None
						return True
					elif cur_node.next is not None:#删除的元素位于中间节点
						cur_node.pre.next = cur_node.next
						cur_node.next.pre = cur_node.pre
						return True
					else:#删除的元素位于尾部
						cur_node.pre.next = cur_node.next
						return True
				else:
					cur_node = cur_node.next

			return False
						


	def research(self,item):
		if self.is_empty():
			return False
		else:
			cur_node = self.__head
			while cur_node is not None:
				if cur_node.item == item:
					return True
				else:
					cur_node = cur_node.next
			return False
	
	def travel(self):
		if self.is_empty():
			return 
		else:
			cur_node = self.__head
			while cur_node is not None:
				print(cur_node.item)
				cur_node = cur_node.next
					

	def is_empty(self):
		return self.__head is None


	def length(self):
		cur_node = self.__head
		count = 0
		while cur_node is not None:
			count += 1
			cur_node = cur_node.next
	
		return count


	
if __name__ == '__main__':
	link = DoubleDirectionLink()
	print(link.length())
	print(link.is_empty())
	print('*'*10)
	link.add(1)
	print(link.length())
	print(link.is_empty())
	print('*'*10)
	print(link.research(1))
	print(link.research(2))
	print('*'*10)
	print(link.remove(2))
	print(link.remove(1))
	print(link.length())
	print(link.is_empty())
	print('*'*10)

	link.insert(2,1)
	link.insert(-1,3)
	link.add(3)
	link.insert(3,1)
	link.insert(0,5)
	link.append(6)
	link.travel()
	print(link.is_empty())
	print('*'*10)
	
	link.remove(5)
	link.remove(6)
	link.travel()
	print('*'*10)
	
