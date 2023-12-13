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

    def reverse2(self):
        """递归法反转链表2，到达终点后回溯"""

        def inner_reverse(node):
            if node.next is None:   #到达尾部
                self._root.next = node
                return node

            get_node = inner_reverse(node.next)
            get_node.next = node
            return node

        first_node = self._root.next
        if first_node:
            inner_reverse(first_node)
        else:
            return
        first_node.next = None


    def seq_reverse(self):
        """来链表从前向后地反转
            a,b,c 三个指针分别一次相邻，反转的时候，先让b.next=a 反转前两个，然后a=b,相当于a指针后移一位
            同时b=c，b也向后移一位，c=c.next c也向后移一位，在反复循环上述过程，直到链表终点；
            在链表末尾时，c=c.next将，c将会是None，但是因为a，b重新移位后还没有建立连接，但是c已经是None了无法在进行下一次的一位，所以，循环终止，在循环终止后，需要再加一次 b.next=a；最后把链表头指向原尾部节点b即可
        """

        a = self._root.next
        b = a.next
        if b is None:return
        a.next = None
        c = b.next
        while c is not None:
            b.next = a
            a = b
            b = c
            c = b.next
        b.next = a

        self._root.next = b


l1 = Link()
for i in range(10):
    l1.append(i)
l1.travel()
# l1.reverse()
# l1.seq_reverse()
l1.reverse2()
l1.travel()