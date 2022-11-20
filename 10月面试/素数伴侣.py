'''
题目描述
若两个正整数的和为素数，则这两个正整数称之为“素数伴侣”，如2和5、6和13，它们能应用于通信加密。现在密码学会请你设计一个程序，从已有的 N （ N 为偶数）个正整数中挑选出若干对组成“素数伴侣”，挑选方案多种多样，
例如有4个正整数：2，5，6，13，如果将5和6分为一组中只能得到一组“素数伴侣”，而将2和5、6和13编组将得到两组“素数伴侣”，能组成“素数伴侣”最多的方案称为“最佳方案”，当然密码学会希望你寻找出“最佳方案”。
输入:
有一个正偶数 n ，表示待挑选的自然数的个数。后面给出 n 个具体的数字。

输出:
输出一个整数 K ，表示你求得的“最佳方案”组成“素数伴侣”的对数。

数据范围：1≤n≤100  ，输入的数据大小满足 2≤val≤30000
输入描述：
输入说明
1 输入一个正偶数 n
2 输入 n 个整数

输出描述：
求得的“最佳方案”组成“素数伴侣”的对数。

示例1
输入：
4
2 5 6 13
输出：
2
示例2
输入：
2
3 6
输出：
0
'''
def is_primer(v1,v2):
    # 判断是否素数
    n = v1+v2
    if n == 1 or n ==2:
        return True
    for v in range(2, n // 2 + 1):
        r, m = divmod(n, v)
        if r > 0 and m == 0:
            return False
    return True



def main():
    quantity = int(input().strip())
    nums = list(map(int,input().strip().split()))

    odds,evens = [],[]
    for each in nums:
        if each %2 == 0:
            evens.append(each)
        else:
            odds.append(each)

    arr = [[False for _ in range(len(evens))] for _ in range(len(odds))]
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] = is_primer(odds[i],evens[j])

    # print(arr)

    evens_match = [-1 for _ in range(len(evens))]
    def match(oi):
        for j in range(len(evens)):
            if arr[oi][j] and not evens_visited[j]:
                evens_visited[j] = True
                if evens_match[j] == -1 or match(evens_match[j]):
                    evens_match[j] = oi
                    return True
        return False

    cnt = 0
    for i in range(len(odds)):
        evens_visited = [False for _ in range(len(evens))]
        if match(i):
            cnt += 1
    print(cnt)


if __name__ == '__main__':
    main()

