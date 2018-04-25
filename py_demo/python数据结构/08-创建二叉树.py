#coding:utf-8


class Node(object):
	"""二叉树节点"""
	def __init__(self,item):
		self.item = item
		self.lchild = None
		self.rchild = None
	

class Tree(object):
	def __init__(self,node=None):
		self.root = node
	
	def add(self,item):
		node = Node(item)
		if self.root is None:
			self.root = node
			return
		queue = [self.root]
		while queue:
			cur_node = queue.pop(0)
			if cur_node.lchild is None:
				cur_node.lchild = node
				return
			else:
				queue.append(cur_node.lchild)

			if cur_node.rchild is None:
				cur_node.rchild = node
				return
			else:
				queue.append(cur_node.rchild)
		


	def breadth_travel(self):
		"""广度遍历"""
		if self.root is None:
			return
		queue = [self.root]
		while queue:
			cur_node = queue.pop(0)
			print(cur_node.item)
			if cur_node.lchild is not None:
				queue.append(cur_node.lchild)
			if cur_node.rchild is not None:
				queue.append(cur_node.rchild)

	
	def preorder(self,node):
		"""先序遍历"""
		if node is None:
			return
		print(node.item)
		self.preorder(node.lchild)
		self.preorder(node.rchild)
			
	def postorder(self,node):
		"""后序便利"""
		if node is None:
			return

		self.postorder(node.lchild)
		self.postorder(node.rchild)
		print(node.item)

	
	def middleorder(self,node):
		if node is None:
			return
		self.middleorder(node.lchild)
		print(node.item)
		self.middleorder(node.rchild)


if __name__ == '__main__':
	tree = Tree()
	tree.add(0)
	tree.add(1)
	tree.add(2)
	tree.add(3)
	tree.add(4)
	tree.add(5)
	tree.add(6)
	tree.add(7)
	tree.add(8)
	tree.add(9)
	tree.add(10)

	tree.breadth_travel()
	print('*'*10)
	tree.preorder(tree.root)
	print('*'*10)
	tree.postorder(tree.root)
	print('*'*10)
	tree.middleorder(tree.root)
