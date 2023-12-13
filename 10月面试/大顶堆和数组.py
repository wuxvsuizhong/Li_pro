# 按照数组的形式，整理打定堆，
# h为堆的高度，i为元素的的数组下标，那么有以下规律
# h从顶层高度为0开始计数，那么某一层的子顶堆的左右子节点，左节点为2*i+1 ，右节点为2*i+2
# 父节点的位置为(i-1)/2
# li=[0,1,2,3,4,5,6...]
# 下标0为堆的顶部。那么，1,2分别为0的左右子节点，再向下，3,4分别是1的左右节点，5，6为2的左右节点
# 随便选择一个节点，反推其父节点，如，3，根据(i-1)/2计算，父节点下标为1 满足
# 在随便选个节点推算其子节点的下标,如4,其左节点为(2*4)+1=9,右节点为(2*4)+2=10
#                         0
#                      /      \
#                     1         2
#                    / \      /  \
#                   3   4    5    6
#                  / \ / \  /  \  / \
#                 7  8 9 10 11 12 13 14
# 堆中的数据值均为数据在数组中的下标
import random
import sys
import typing

# 给定一组数据，构建一个大顶堆

class Myheap:
    def __init__(self,limit=sys.maxsize):
        self.__heap = list()
        self.__limit = limit
        # self.__heapsize=0

    def is_empty(self):
        return len(self.__heap) == 0

    def is_full(self):
        return len(self.__heap) == self.__limit

    def push(self,n):
        if len(self.__heap) == self.__limit:
            raise Exception("堆已满")
        self.__heap.append(n)
        self._heap_insert(n,len(self.__heap)-1)
        # self.show()

    def _heap_insert(self,n,index):
        # parent_index = int((index-1)/2)    # 父节点的在数组中的下标序号
        while self.__heap[index] > self.__heap[int((index-1)/2)]: # 如果下标index的数据大于父节点的数据，那么交换
            self.__heap[index],self.__heap[int((index-1)/2)] = self.__heap[int((index-1)/2)],self.__heap[index]
            index = int((index-1)/2) # 当前节点转到父节点上，然后继续和上面的节点比较

    def pop(self):
        """每次弹出顶上的数据"""
        if not self.__heap: return
        ans = self.__heap[0]
        self.__heap[-1],self.__heap[0] = self.__heap[0],self.__heap[-1]  # 交换顶部节点和最末端位置的节点
        self.__heap.pop()
        self._heapfy(0,len(self.__heap)-1) # 将最末端的节点排除在有效的数据范围之外

        return ans

    def _heapfy(self,index,heapsize):
        """从某个节点index开始向下遍历左右子节点，如果子节点中有大于index的，交换较大者和index的位置
        交换后，index下沉，继续遍历index的左右子节点，持续这个比较过程，直到index下沉到正确位置
        """
        left = 2*index + 1

        while left <= heapsize: # 如果能够找到左右节点，然后找出左右节点的较大者
            lagest_index = left+1 if (left + 1 <= heapsize and  self.__heap[left] < self.__heap[left+1]) else left
            if self.__heap[lagest_index] > self.__heap[index]: # 子节点较大者与imdex交换
                self.__heap[lagest_index],self.__heap[index] = self.__heap[index],self.__heap[lagest_index]

            elif self.__heap[lagest_index] == self.__heap[left]: break  # 如果发现index位置的值和左右子节点中较大者的值相等的，那么终止比较
            index = lagest_index  # index下沉到左右子节点较大者的位置
            left = index * 2 + 1  # 继续向下遍历，重复比较过程

    # 大顶堆的heapfy过程和insert的过程其实就是相反的流程，前者是index节点向下沉到正确的为止，后者是新加入的节点从尾部向上浮动到正确的为止
    def show(self):
        print(self.__heap)


li = [random.randint(0,100) for _ in range(15)]
print(li)
mq = Myheap()
for n in li:
    mq.push(n)
mq.show()
mq.pop()
mq.pop()
mq.show()


# 堆排序
# 给定一组数据，使用堆排序
# 流程如下，先把数据构建为大顶堆，然后每次pop出堆顶部的元组放置在尾部，当堆中所有的数据都弹出完成后，排序完成

li = [random.randint(0,100) for _ in range(10)]
# li = [98, 59, 21, 70, 45, 89, 43, 23, 72, 53]
print('-'*20,'堆排序','-'*20)
print(li)
mq = Myheap()
for n in li:
    mq.push(n)
mq.show()
sort_li = li[:]
for i in range(len(li)-1,-1,-1):
    ans = mq.pop()
    print(i,ans)
    sort_li[i] = ans

print(sort_li)



