#!/usr/bin/env python
#假设一个数字有n位，这n位数字加和为s,给定s和n,求得组成数字最小的组合
#如，n=2;s=9 那么组成的最小的两位数就是18（1+8=s=9）

#思路：因为s一定，就是组成数字的各个数字之和一定，所以如果要使得数字最小，那么高位数字就不能是大的数，大的数字只能在低位
#而单个每一位数字最大只能是9，所以大的数字尽量分到低位，小的数字分到高位


def findSmallest(s,l):
    if s > l*9:
        return None
    result=[]
    for i in range(l):
        if s > 9:
            s -= 9
            result.append('9')
        elif 1 < s <= 9:
            if i < l - 1:  #轮询未到最高位置
                result.append(str(s-1))
                s = 1
            else:
                result.append(str(s))
                s = 0
        elif s == 1:
            if i < l - 1:
                result.append('0')
            else:
                result.append('1')
                s = 0
        else:
            pass
    
    print(result)
    result.reverse()
    return int(''.join(result))


if __name__ == '__main__':
    tups = [(9,2),(20,3),(26,3),(3,4)]
    for s,l in tups:
        print(findSmallest(s,l))
