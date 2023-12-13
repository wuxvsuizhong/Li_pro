'''
一个密码锁由 4 个环形拨轮组成，每个拨轮都有 10 个数字： '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' 。每个拨轮可以自由旋转：例如把 '9' 变为 '0'，'0' 变为 '9' 。每次旋转都只能旋转一个拨轮的一位数字。

锁的初始数字为 '0000' ，一个代表四个拨轮的数字的字符串。

列表 deadends 包含了一组死亡数字，一旦拨轮的数字和列表里的任何一个元素相同，这个锁将会被永久锁定，无法再被旋转。
字符串 target 代表可以解锁的数字，请给出解锁需要的最小旋转次数，如果无论如何不能解锁，返回 -1 。

示例 1:
输入：deadends = ["0201","0101","0102","1212","2002"], target = "0202"
输出：6
解释：
可能的移动序列为 "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202"。
注意 "0000" -> "0001" -> "0002" -> "0102" -> "0202" 这样的序列是不能解锁的，因为当拨动到 "0102" 时这个锁就会被锁定。

示例 2:
输入: deadends = ["8888"], target = "0009"
输出：1
解释：
把最后一位反向旋转一次即可 "0000" -> "0009"。

示例 3:
输入: deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
输出：-1
解释：
无法旋转到目标数字且不被锁定。
示例 4:

输入: deadends = ["0000"], target = "8888"
输出：-1


提示：

1 <= deadends.length <= 500
deadends[i].length == 4
target.length == 4
target 不在 deadends 之中
target 和 deadends[i] 仅由若干位数字组成
'''
import queue

deadends = input().strip().split()
target = input().strip()

'''
这道题的考点是广度优先搜索，
广度优先搜索注意的点是，队列的入队和出队，以及注意对队列元素的入队的剪枝，避免对已经检验过的数据做重复入队，造成死循环
可以通过列表或者哈希类记录已经访问过的元素，进行剪枝，否则将陷入队列始终不为空的死循环
'''

status_queue = queue.Queue()    #队列
seen  = [] # 作为对已经入队过的元素的记录，避免重复入队
def bfs():
    if target == "0000":
        return 0
    if "0000" in deadends:
        return -1

    num_prev = lambda x:chr(ord(x)-1) if x != '0' else '9'
    num_next = lambda x:chr(ord(x)+1) if x != '9' else '0'

    def get(grp):
        ret=[]
        cur_grp = grp[0]
        cur_step = grp[1]
        for i,val in enumerate(cur_grp):
            lgrp = list(cur_grp)
            lgrp[i] = num_prev(val)
            ret.append((''.join(lgrp),cur_step+1))

            lgrp[i] = num_next(val)
            ret.append((''.join(lgrp),cur_step+1))
        return ret

    status_queue.put(('0000',0))
    seen.append(('0000',0))
    while not status_queue.empty():
        proc_grp,step = status_queue.get()
        if proc_grp == target:
            return step

        for each in get((proc_grp,step)):
            if (each[0] not in deadends) and (each[0] not in seen):
                status_queue.put(each)
                seen.append(each[0])

    return -1


print(bfs())






