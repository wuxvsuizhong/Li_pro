#!/usr/bin/env python

#给定一系列的活动的开始时间和结束时间，有可能存在着安排的活动时间冲突
#从中筛选出不冲突的最多能够安排的活动个数

def MaxActivites(acts):
    #对每个活动按照结束时间排序从小到大
    sort_acts = sorted(acts,key=lambda tup: tup[1])
    prev = sort_acts[0]
    print(prev)
    result = [prev]
    for cur in sort_acts:
        if cur[0] > prev[1]:
            #如果下一个活动的开始时间晚于前一个活动的结束时间,那么说明该活动可以安排，接入到result中
            result.append(cur)
            prev = cur
    
    return result


if __name__ == '__main__':
    acts=[(0,6),(3,4),(1,2),(5,7),(8,9),(5,9)]
    ret = MaxActivites(acts)
    print(ret)

