#!/usr/bin/env python
#给定一个数字，将其拆分为两个子数组，再将两个子数组的数字分别按位组成两个较小的数字，使得两数的和最小
#组成的数字中0可以在最高位


#分析:要使得两个数字的和最小，那么两个数字就要是最小的.
#给数组从小到大排序，然后轮询子数组1和子数组2不断从排序后的数组中选取，组成两个最小的数


import heapq

def minSum(li):
    heapq.heapify(li)
    num1 = 0
    num2 = 0
    while li:
        num1 = num1*10 + heapq.heappop(li)
        if li:
            num2 = num2*10 + heapq.heappop(li)
    
    print(num1,num2)
    return num1 + num2

if __name__ == '__main__':
    li=[0, 4, 1, 7, 6, 3, 2, 9]
    print(minSum(li))
    li=[6,8,4,5,2,3]
    print(minSum(li))
    li=[5,3,0,7,4]
    print(minSum(li))
