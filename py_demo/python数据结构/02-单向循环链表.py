# -*- coding:utf-8 -*-




class Node(object):
	def __init__(self,item=None):
		self.item = item
		self.next = None


class CircleLink(object):
	def __init__(self,node=None):
		self.__head = node
		if node:
			node.next = node
	
	def add(self,item):
		new_Node = Node(item)
		head_Node = self.__head
		if self.is_empty():
			self.__head = new_Node
			new_Node.next = new_Node
		else:
			self.__head = new_Node
			new_node.next = head_Node
			cur_Node = head_Node
			while cur_Node.next != head_Node:
				cur_Node = cur_Node.next
			cur_Node.next = new_Node


	def is_empty(self):
		return self.__head == None
	
	def length(self):
		cur_Node = self.__head
		if cur_Node == None:
			return 0
		count = 1 
		while cur_Node.next != self.__head:
			count += 1;
			cur_Node = cur_Node.next

		return count
	
	def append(self,item):
		new_Node = Node(item)
		if self.is_empty():
			self.__head = new_Node
			new_Node.next = new_Node
			return True

		cur_Node = self.__head
		while cur_Node.next != self.__head:#调到尾部节点
			cur_Node=cur_Node.next

		cur_Node.next = new_Node
		new_Node.next = self.__head#循环链接链表头

		return True
	
	def insert(self,pos,item):
		if self.is_empty():
			self.add(item)
			return
		length = self.length();
		if pos > length:
			self.append(item)
			return
		elif pos <= 0:
			self.add(item)
			return 

		cur_Node = self.__head
		front = None
		for i in range(pos-1):
			front = cur_Node
			cur_Node = cur_Node.next
		ret = Node(item)
		front.next = ret
		ret.next = cur_Node

	def travel(self):
		if self.is_empty():
			return
		cur_Node = self.__head
		while cur_Node.next != self.__head:
			print(cur_Node.item)
			cur_Node = cur_Node.next
		print(cur_Node.item)
	
	def remove(self,item):
		if self.is_empty():
			return False

		cur_Node = self.__head
		front = self.__head 
		while cur_Node.next != self.__head:#单个节点的时候不满足，并且跳出循环后cur_Node指向尾部节点
			if cur_Node.item == item:
				if cur_Node == self.__head:#如果是位于头结点
					while cur_Node.next != self.__head:#找到尾部节点
						cur_Node = cur_Node.next
					cur_Node.next = self.__head.next
					self.__head = self.__head.next
					return True
				else:
					front.next = cur_Node.next

				return True
			else:
				front = cur_Node
				cur_Node = cur_Node.next
		#跳出循环或者不执行循环的情况1-链表只有一个节点，2-虚幻迭代到最后一个节点，但是此时最后一个节点没有做值的比较判断
		if cur_Node.item == item:
			if cur_Node == front:#如果是单个的节点
				self.__head = None
			else:#如果是迭代到最后的节点
				front.next = self.__head
			return True
		else:
			return False
		
	
	def research(self,item):
		if self.is_empty():
			return False
		cur_Node = self.__head
		while cur_Node.next != self.__head:
			if cur_Node.item == item:
				return True
			else:
				cur_Node = cur_Node.next
		if cur_Node.item == item:
			return True

		return False


if __name__ == '__main__':
	circle_link = CircleLink()
	print(circle_link.length())
	print(circle_link.is_empty())
	circle_link.add(1)
	print('*'*10)
	print(circle_link.length())
	print(circle_link.is_empty())
	print(circle_link.remove(1))
	print('*'*10)
	print(circle_link.length())
	print(circle_link.is_empty())
	
	
	circle_link.insert(3,1)
	print('*'*10)
	print(circle_link.length())
	print(circle_link.is_empty())

	circle_link.append(2)
	circle_link.append(3)
	circle_link.append(4)
	circle_link.append(5)
	circle_link.append(6)
	print('*'*10)
	print(circle_link.length())
	print(circle_link.is_empty())
	circle_link.travel()


	circle_link.insert(2,22)
	circle_link.insert(3,33)
	print('*'*10)
	#print(circle_link.length())
	circle_link.travel()

	ret = circle_link.research(6)
	if not ret:
		print('not found')
	
	print('*'*10)
	print(circle_link.remove(4))
	circle_link.travel()
