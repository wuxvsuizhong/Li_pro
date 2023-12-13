# 常用语求解链表中点问题
"""
1.给定链表头结点，如果链表长度为奇数，返回链表中点，偶数长都返回链表上中点
2.给定链表头结点，如果链表长度是奇数，返回链表中点，偶数长度返回链表下中点
3.给出链表头结点，如果链表长度是奇数，返回中点的前一个节点，偶数长度，返回链表上中点的前一个
4.给出链表头结点，如果链表长度实际数，返回中点的前一个节点，偶数长度，返回链表下中点的前一个
"""

# 统一认为莲表头节点就是数据节点的头结点
def mid_or_upmid_node(head):
    """1.给定链表头结点，如果链表长度为奇数，返回链表中点，偶数长都返回链表上中点"""
    if (head is None) or (head.next is None) or (head.next.next is None):
        return head
    slow,fast = head.next,head.next.next
    while fast.next and fast.next.next: # 快指针达到最后一个节点时，停止遍历
        slow = slow.next
        fast = fast.next.next
    return slow

def mid_or_downmid_node(head):
    """2.给定链表头结点，如果链表长度是奇数，返回链表中点，偶数长度返回链表下中点"""
    if (head is None) or (head.next is None):
        return head
    slow,fast = head.next,head.next
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# 思考的技巧就是结合起始位置的快慢指针slow和fast位于head的偏移位置，从2节点，3节点，4节点开始，推敲具体情况即可

def premid_or_preupmid_node(head):
    """3.给出链表头结点，如果链表长度是奇数，返回中点的前一个节点，偶数长度，返回链表上中点的前一个
"""
    if (head is None) or (head.next is None) or (head.next.next is None):
        return None
    slow,fast = head,head.next.next
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def premid_or_predownmid_node(head):
    """4.给出链表头结点，如果链表长度实际数，返回中点的前一个节点，偶数长度，返回链表下中点的前一个"""
    if head is None or head.next is None:
        return None
    slow,fast = head,head.next
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow




