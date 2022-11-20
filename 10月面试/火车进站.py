'''
给定一个正整数N代表火车数量，0<N<10，接下来输入火车入站的序列，一共N辆火车，每辆火车以数字1-9编号，火车站只有一个方向进出，同时停靠在火车站的列车中，只有后进站的出站了，先进站的才能出站。
要求输出所有火车出站的方案，以字典序排序输出。
数据范围：1≤n≤10
进阶：时间复杂度：O(n!)\O(n!) ，空间复杂度：O(n)\O(n)
输入描述：
第一行输入一个正整数N（0 < N <= 10），第二行包括N个正整数，范围为1到10。

输出描述：
输出以字典序从小到大排序的火车出站序列号，每个编号以空格隔开，每个输出序列换行，具体见sample。

示例1
输入：
3
1 2 3

输出：
1 2 3
1 3 2
2 1 3
2 3 1
3 2 1

说明：
第一种方案：1进、1出、2进、2出、3进、3出
第二种方案：1进、1出、2进、3进、3出、2出
第三种方案：1进、2进、2出、1出、3进、3出
第四种方案：1进、2进、2出、3进、3出、1出
第五种方案：1进、2进、3进、3出、2出、1出
请注意，[3,1,2]这个序列是不可能实现的。
'''
quantity = int(input().strip())
outnumstack = list(map(int,input().strip().split()))
# outstack = []
station = []
res = []

def search(outstack,station,numstack):
    print(numstack)
    if not station and not numstack:
        res.append(outstack)
        return

    outnums = numstack[:]
    ostack = outstack[:]
    cnumstack = numstack[:]
    # 火车出站
    if station:
        for each in station:
            outnum = station.pop()
            outstack.append(outnum)
            search(outstack,station,numstack)
    # 火车选择不出站，选择入站
     # 先恢复现场
    station=outnums[:]
    outstack=ostack[:]
    numstack=cnumstack[:]
     # 火车入站
    if numstack:
        for each in numstack:
            innum = numstack.pop(0)
            station.append(innum)
            search(outstack,station,numstack)


search([],[],outnumstack)
print(res)