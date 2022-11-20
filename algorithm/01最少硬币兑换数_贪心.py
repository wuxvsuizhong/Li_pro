#!/usr/bin/env python

def minCoins(nums,total):
    coins = sorted(nums)
    coins.reverse() 
    result=[]
    for c in coins:
        ret = total//c
        mod = total%c
        if mod > 0:
            total = mod
            result.append(ret)
        elif mod == 0:
            result.append(ret)
            break
     
    print(result)
    return sum(result)


if __name__ == '__main__':
    coins=[1,5,10,20,50,100]
    ret = minCoins(coins,1006)
    print(ret)
