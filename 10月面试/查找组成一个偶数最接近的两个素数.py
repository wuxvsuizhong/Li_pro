'''
任意一个偶数（大于2）都可以由2个素数组成，组成偶数的2个素数有很多种情况，本题目要求输出组成指定偶数的两个素数差值最小的素数对。

数据范围：输入的数据满足 4≤n≤1000
输入描述：
输入一个大于2的偶数

输出描述：
从小到大输出两个素数

示例1
输入：
20
输出：
7
13

示例2
输入：
4
输出：
2
2
'''
def is_primer(num):
    if 0 < num <= 2:
        return True
    for v in range(2,num//2):
        if num % v == 0:
            return False
    return True

def main():
    n = int(input().strip())
    minval = [0,n]
    for v in range((n//2)+1):
        r = n-v
        if is_primer(v) and is_primer(r):
            if r-v <= abs(minval[1]-minval[0]):
                minval=[v,r]

    minval.sort()
    for each in minval:
        print(each)


if __name__ == '__main__':
    main()