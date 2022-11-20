class LinkNode:
    def __init__(self,n):
        self.num = n
        self.next = None

class Link:
    def __init__(self):
        self._root = LinkNode(-1)

    def append(self,n):
        '''在链表末尾追加节点'''
        head = self._root

        while head.next:
            head = head.next
        head.next = LinkNode(n)

    def travel(self):
        '''遍历链表'''
        head = self._root
        while head.next:
            head = head.next
            print(head.num,end=' ')
        print()

    def reverse(self):
        '''递归地反转链表'''
        node = self._root.next

        def start_reverse(node):
            if not node or not node.next:
                self._root.next = node
                return

            start_reverse(node.next)
            node.next.next = node
            node.next = None
            # return node
            return

        start_reverse(node)

l1 = Link()
for i in range(10):
    l1.append(i)
l1.travel()
l1.reverse()
l1.travel()