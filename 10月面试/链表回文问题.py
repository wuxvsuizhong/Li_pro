# 给定一个链表头结点，判断链表的数据从头到尾是否是回文
# 如莲表从头到尾部的数据是 a-b-g-b-a 那么链表是回文

"""
这时候可使用栈结构解决，从头到尾遍历链表，并依次把莲表数据压栈，然后在从栈顶依次出栈
在从头遍历链表，如果出栈的顺序和俩表的遍历顺序是一样的，那么链表是回文

这是利用了回文无论是正向还是反向，遍历的时候，顺序是一致的这一特性
"""
import collections

def check_link_balance(link):
    stack = collections.deque()
    for each in link:
        stack.append(each)

    for val in link:
        if stack.pop() != val:
            return False
    return True

link = 'abcde'
print(check_link_balance(link))
link = 'abcba'
print(check_link_balance(link))
link = 'a'
print(check_link_balance(link))
link = 'aa'
print(check_link_balance(link))

"""
另外一种节省空间的办法是，使用快慢指针，当链表个数为偶数的时候，定位到下中点，当莲表长度为奇数的时候，定位到中点的下一个节点。
然后把莲表的中点后面的节点从前到后依次压栈，那么完成后，栈中按照出栈顺序，就应该是后半段的逆序。
然后从头结点开始向后遍历链表的前半段，每次和出栈的值比较，只要中间有一个出栈的值和链表遍历的值不一样，那么就不是回文，当所有的前半段链表遍历完成，并且与栈中的出栈的元素按个比较的值是一样的，那么就是回文
"""

def downmid(head):
    """链表长度为偶数时，返回链表的下中点，如果是奇数，返回链表的中点的下一个节点"""
    if head is None or head.next is None or head.next.next is None:
        return None
    slow,fast = head.next.next,head.next.next
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def check_link_balance(link):
    # down_mid = downmid(link)
    down_mid = int((len(link)+1)/2)
    stack = collections.deque()
    for each in link[down_mid:]:
        stack.append(each)
    if len(stack) == len(link[:down_mid]):  # 链表长度为偶数
        for each in link[:down_mid]:
            if each != stack.pop(): return False
    else:
        for each in link[:down_mid-1]:
            if each != stack.pop(): return False
    return True


print(check_link_balance('abc'))
print(check_link_balance('aba'))

"""
还有一种是不借助栈的方式，对于链表，仍然是需要使用快慢指针定位到中点，然后把链表中中点往后的节点逆序。
然后依次遍历链表已经逆序的后半段从头(逆序前是链表的尾部)开始到终点，以及原版莲表的头的前半段开始逐个比对，如果中间有一个节点的值不相等那么就不是回文，比较完成后，如果各两两比较的结果都是相等的，那么链表是回文
"""
