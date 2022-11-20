'''
对于长度为n的一个字符串A（仅包含数字，大小写英文字母），请设计一个高效算法，计算其中最长回文子串的长度。
数据范围:10001≤n≤1000
要求：空间复杂度 O(1)O(1)，时间复杂度 O(n^2)O(n^2)
进阶:  空间复杂度 O(n)O(n)，时间复杂度 O(n)O(n)
示例1
输入：
"ababc"
返回值：
3
说明：
最长的回文子串为"aba"与"bab"，长度都为3

示例2
输入：
"abbba"
返回值：
5

示例3
输入：
"b"
返回值：
1
'''


def main():
    s = input().strip()
    res = []

    maxlen = 0
    for i in range(0, len(s)):
        l,r = i,i+1
        while 0 <= l < len(s) and 0 <= r < len(s):
            if s[l] == s[r]:
                maxlen = max(maxlen,r-l+1)
                res.append(s[l:r+1])
                l,r = l-1,r+1
            else:
                break

    for i in range(1, len(s)):
        l,r = i-1,i+1
        while 0 <= l < len(s) and 0 <= r < len(s):
            if s[l] == s[r]:
                maxlen = max(maxlen,r-l+1)
                res.append(s[l:r+1])
                l,r = l-1,r+1
            else:
                break

    print(maxlen)

def dp_process():
    s = input().strip()
    res = []

    dp = [[False for _ in range(len(s))] for _ in range(len(s))]
    for i in range(len(s)):
        for j in range(len(s)):
            if i == j:
                dp[i][j] = True


    for i in range(len(s)):
        for j in range(i):
            if s[i] == s[j] :
                if i-j <= 2:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i-1][j+1]
            else:
                dp[i][j] = False

            if dp[i][j] and s[j:i+1]:
                res.append(s[j:i+1])
    return res

if __name__ == '__main__':
    # main()
    res = dp_process()
    print(res)