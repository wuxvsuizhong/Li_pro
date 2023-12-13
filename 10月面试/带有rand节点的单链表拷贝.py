"""
一种特殊的单链表，其节点除了携带的数据，以及next指针，还有一个rand指针，该rand指针可能指向链表中的任意的其他节点，也可能指向None

【要求】时间复杂福O(n),额外空间复杂度O(1)实现一种方法能够，复制链表
"""
import copy
import random

from LinkList import Link
class Node:
    def __init__(self,var,rand_node=None,next=None):
        self.var = var
        self.rand = rand_node
        self.next = next
    def __repr__(self):
        """这里为了验证拷贝的效果，使用id打印对象的内存地址"""
        return f'[ Node:->({id(self)} var:{self.var}, rand:{self.rand}) ]'


class SpecialLink(Link):
    def __init__(self):
        super().__init__()

    def add(self,num:int):
        if self._head is None:
            rand_index = random.randint(-1,len(self))
            rand_node = self[rand_index]
            self._head = Node(num,rand_node)
            return
        node = self._head
        while node.next:
            node = node.next
        rand_index = random.randint(0, len(self))
        print('rand_index:', rand_index)
        rand_node = self[rand_index]
        node.next = Node(num,rand_node)

    def travel(self):
        node = self._head
        while node:
            print(node)
            node = node.next
        print()


    def link_copy_hash(self):
        """借助hash字典，进行链表拷贝"""
        if not self._head: return None
        node = self._head
        map = {}   # map就是链表拷贝的精髓所在
        while node: # 记录原本链表的node和拷贝的链表的cp_node的映射关系
            # map[node] = copy.copy(node)
            map[node] = Node(node.var,node.rand,node.next)
            node = node.next

        # 在拷贝链表cp_link没有还原之前，cp_node中的节点的next和rando指向还是原链表的节点
        for origin_node in map:  # 迭代mao中所有的拷贝节点cp_node,把拷贝的节点的next和rando指向关系，指向转为cp_link中的节点
            cp_node = map[origin_node]
            cp_node.next = map[origin_node.next] if origin_node.next else None
            cp_node.rand = map[origin_node.rand] if origin_node.rand else None

        cp_link = SpecialLink()  # 构建拷贝的链表对象
        cp_link._head = map[self._head] # 新链表的头结点指定为拷贝链表的头
        return cp_link # 返回复制的链表


    def link_copy_nohash(self):
        """不借助hash字典，复制链表"""
        if not self._head:return None
        first = self._head
        while first:
            # 复制每一个链表节点的副本，追加插入到原节点的后面
            cp_node =  Node(first.var,first.rand,first.next)
            second = first.next
            first.next = cp_node
            cp_node.next = second
            first = second

        print('before split：')
        self.travel()

        cp_head = self._head.next
        node = self._head
        while node:  # 先整理链表中，复制的节点的randon的值
            cp_node = node.next
            cp_node.rand = cp_node.rand.next if cp_node.rand else None
            node = cp_node.next


        node = self._head
        while node: # 然后再拆分链表中，复制节点和原来节点拆分为两条链表
            cp_node = node.next
            node.next = cp_node.next if cp_node.next else None
            cp_node.next = node.next.next if node.next else None
            node = node.next

        # 这里需要先更新random的值，然后在拆分，两个while合在一起的时候，总是会拆分失败，需要拆成两个while
        # 原因在于，如果一边更新random一边拆分，当尾部节点引用头部节点这种情况时，如果已经在头部节点把原节点和其复制节点相邻的连接拆开了，那么就无法在通过random访问的原节点，找到其复制节点了
        new_link = SpecialLink()
        new_link._head = cp_head
        return new_link

if __name__ == "__main__":
    l = SpecialLink()
    for i in range(10):
        l.add(i)
    l.travel()

    cp_l = l.link_copy_hash()
    print('cpy_hash')
    cp_l.travel()   # 需要域原链表l的travel函数遍历的结果一致

    print('cpy_nohash')
    cp_l2 = l.link_copy_nohash()
    print('l.travel')
    l.travel()

    print('cp_l2.travel')
    cp_l2.travel()

"""
给定两个可能是换也有可能无环的单链表，头结点head1和head2.请实现一个函数，如果两个链表相交，返回相交的第一个交点。
如果不想交，返回null

【要求】如果两个链表长度之和为N,时间复杂度请达到O(N),额外空间复杂度达到O(1)

####关于单链表的环路的说明####
关于单链表，如果存在这环，那么在入环之后，是无法再出环的，因为在入环的节点处之后单项的指针始终指向环内，当环走完一圈之后，回到乳环的位置，就会继续在环中流转，无法出环，形状类似于“6”，或者是“O”.
如果是两个单链表相交，并且有环路，那么他们必有公共的环且在两条链表入环之后，都无法出环，也就是除了入环方向的链表，无出环的链表分支
形状类似于“只”字型，或者是一个环上，从两个分别不同的点入环。

一个有环而另一个无环的链表，不存在相交的情况，只要相交，必然有公共环。
###########################

###单链表无环时###
如果无环的单链表相交，那么，他们必然中终止与公共的部分，类似于Y字型
################

这个问题的解法，需要先判断链表是否有环，如果有环，按照有环方式处理，而如果无环，按照无环的方式处理
"""

def check_link_ring(head):
    """给定一个单链表的头结点，判读链表是否有环路，如果有，返回入环的第一个节点"""
    def use_set_check(): #方式一：使用set检测链表是否有环
        """如果是存在环路，那么在入环后重复环内循环时，必然会有重复访问的节点的情况存在"""
        if not head: return None
        node = head
        set1=set()
        while node:
            if node in set1: # 如果set中存在着之前访问过的节点，那么是环路，返回True
                return node
            set1.add(node)
            node = node.next
        return None # 如果没有在while中return，那么不是环路

    def fast_slow_check(): # 方式2：使用快慢指针，快指针单步移动为2，慢指针单步移动1
        """快慢指针判断是否有环，初始状态，快慢指针分别位于头结点和next节点上，如果有环则快慢指针必然在环内相交
        规律：当快慢指针第一次相交后，快指针返回头结节点，然后快指针退化为单步走1(直接快指针回到头节点这一步时，慢指针同时也需要向前走一步)，那么此时，继续快和慢指针同步走，当快慢指针再次相遇的时候，相遇的节点就是入环的第一个节点
        """
        if not head or not head.next: return False
        slow,fast = head,head.next
        while fast and  (slow is not fast):
            slow = slow.next
            fast = fast.next.next
        if not fast: return None # fast达到终点，不是环路
        #循环终止时，slow和fast第一次相遇
        slow = slow.next
        fast = head
        while slow is not fast:
            slow = slow.next
            fast = fast.next
        # 第二次fast和slow相遇的节点就是入环的节点
        return slow

def check_2noring_link_ismeet(head1,head2):
    """检查两个无环的单链表是否相交，相交返回第一个相交的节点"""
    def check_with_hash(): # 方式1：借助hash set检查是否相交
        if not head1 or not head2:
            return False
        node1 = head1
        set1 = set()
        # while node1: # 先把第一个链表各个节点放入set中
        for _ in range(len(head1)): # 使用遍历长度的方式遍历链表比较好
            set1.add(node1)
            node1 = node1.next

        node2 = head2
        # while node2: # 遍历链表2，逐个检查是否在set中存在
        for _ in range(len(head2)): # 使用遍历长度的方式遍历链表比较好
            if node2 in set1:
                return node2 # 发现重复的第一个节点，就是两个无环链表相交的点
            node2 = node2.next

    def chcek_with_noset(): # 方式2：使用长度计数的方式，
        if not head1 or not head2:
            return False
        l1 = 0
        node1 = head1
        while head1: #注意这种方式不适合有坏链表的长度统计,
            l1 += 1
            node1 = node1.next
        # l1 = link1.length() # 或者能有特殊的方式知道有坏链表的长度

        l2 = 0
        node2 = head2
        while node2: #注意这种方式不适合有坏链表的长度统计
            l2 += 1
            node2 = node2.next
        # l2 = link1.length() # 或者能有特殊的方式知道有坏链表的长度


        long_link_herad = head1 if l1 > l2 else head2
        short_link_head = head2 if long_link_herad is head1 else head1
        step = abs(l1-l2)
        l_node = long_link_herad
        for _ in range(step): # 长链表的指针先走step步
            l_node = l_node.next
        s_node = short_link_head
        while (l_node and s_node) and (l_node is not s_node): # 长短两个链表的指针同时走相同的步数
            l_node = l_node.next
            s_node = s_node.next
        #循环结束时，如果都不为空，那么相遇的节点就是相交的节点
        if (l_node and s_node) and (l_node is s_node):
            return s_node

    return check_with_hash()

def check_2ring_link_ismeet(head1,head2):
    """检查两个有环链表的第一个相交节点
    1.如果两个有环链表相交，那么必然存在着公共环。
    2.如果两个有环链表的相交点不是一个点，那么相交的点必然位于环上的不同位置节点。
    3.如果两个有环的链表相交节点是一个点，那么有可能位于环上的同一个节点，或者入环之前的某个交点，此时可以转化为求解两个单链表的第一个相交的点的问题，因为此时链表相交的地方已经与环无关了
    4.如果两个有坏链表不想交，那么他们各自有自己的环路。
    """

    #先找出两个链表的入环节点
    inloop_node1 = check_link_ring(head1)
    inloop_node2 = check_link_ring(head2)
    if inloop_node1 and inloop_node2:
        if inloop_node1 is not inloop_node2:
            # 两个链表的入环节点不一样
            # 那么找随便一个环，在环内循环如果循环过程中始终遇不到另外一个环的入环节点，那么，两个环路链表不相交
            """循环检查是否能在loop1中找到inloop_noide2节点"""
            # 如果有相交，那么说明虽然两个链表有共同的环路，只是，入环交点不在一个位置，所以也没有共同的交点
            return False
        else:
            #两个链表的入环节点一样
            return check_2noring_link_ismeet()























