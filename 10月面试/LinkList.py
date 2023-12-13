import collections
import typing

class Node:
    def __init__(self,var):
        self.var = var
        self.next = None

    def __repr__(self):
        return f'<Node->var:{self.var}>'


class Link:
    def __init__(self):
        self._head = None
        self._len = 0

    def add(self,num:int):
        if self._head is None:
            self._head = Node(num)
            self._len += 1
            return
        node = self._head
        while node.next:
            node = node.next
        node.next = Node(num)
        self._len += 1

    def travel(self):
        node = self._head
        while node:
            print(node.var,end=' ')
            node = node.next
        print()

    def __len__(self):
        return self._len
    def __getitem__(self, index):
        if self._head is None:
            return None
        length = self._len -1
        if abs(index) >length:
            raise IndexError("要访问的下标超出链表长度")
        elif 0<=index<=length:
            node = self._head
            for _ in range(index):
                node = node.next
            return node

    def reverse(self):
        def inner_reverse(node):
            if not node: return None
            next_node = inner_reverse(node.next)
            if not next_node: # 获取的下一个节点为None,说明当前节点是最后一个节点
                self._head.next = None # 先把原来的头结点next指针置空
                self._head = node
            else: # 获取的下一个节点不为空
                next_node.next = node
            return node

        return inner_reverse(self._head)

    def get_head(self):
        return self._head

l = Link()
print(len(l))
for i in range(10):
    l.add(i)
l.travel()
print(len(l))
print(l[2])
# l.reverse()
# l.travel()

# n1 = Node(10)
# n2 = Node(11)
# n3 = Node(10)
# print(n1 is n2)
# print(not n1 is n3)
