'''
给出一个整型数组 numbers 和一个目标值 target，请在数组中找出两个加起来等于目标值的数的下标，返回的下标按升序排列。
（注：返回的数组下标从1开始算起，保证target一定可以由数组里面2个数字相加得到

输入：
[3,2,4],6
返回值：
[2,3]
说明：
因为 2+4=6 ，而 2的下标为2 ， 4的下标为3 ，又因为 下标2 < 下标3 ，所以返回[2,3]
'''
import sys

def main():
    line = list(map(int,sys.stdin.readline().strip().split()))
    nums = line[:-1]
    target = line[-1]
    rec = {}
    for i,v in enumerate(nums):
        rec[v] = i+1

    result=set()
    for i,n in enumerate(nums):
        if target-n in rec and rec[target-n] != i+1:
            tmplist=[i+1,rec[target-n]]
            tmplist.sort()
            result.add(tuple(tmplist))

    print(list(map(list,result))[0])


if __name__ == '__main__':
    main()