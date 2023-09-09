from collections import deque

dq = deque(range(10), maxlen=10)  # 第二个参数是一个可选参数，表示设置deque中最多允许放置多少个数\
print(dq)  # deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)

dq.rotate(3)  # 轮转，当 n>0时，从右边取几项放到左边，当n<0时，从左端取几项放到右端
print(dq)  # deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)

dq.rotate(-4)
print(dq)  # deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)

dq.appendleft(-1)  # 向已满的deque中的一段追加几项，那么另外一段就要丢弃几项
print(dq)  # deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)

dq.extend([11, 22, 33])  # 因为队列已满，向右侧追加3项，会把左侧的3项挤出队列
print(dq)  # deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)

dq.extendleft([10, 20, 30, 40])  # 在队列的左侧追加4项，右侧就会被挤出4项
print(dq)  # deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)
