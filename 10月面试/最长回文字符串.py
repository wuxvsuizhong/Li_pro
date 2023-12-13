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
    """双指针法+中心扩散法"""
    s = input().strip()
    res = []

    maxlen = 0
    for i in range(0, len(s)):  #针对回文字符串长度是偶数的情况
        l,r = i,i+1
        while 0 <= l < len(s) and 0 <= r < len(s):
            if s[l] == s[r]:
                maxlen = max(maxlen,r-l+1)
                res.append(s[l:r+1])
                l,r = l-1,r+1
            else:
                break

    for i in range(1, len(s)):  # 针对会问字符串长度是奇数的情况
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
    """动态规划法"""
    s = input().strip()
    res = []

    dp = [[False for _ in range(len(s))] for _ in range(len(s))]
    # 创建字符串对应的动态规划网格，dp[i][j]代表从i->j的字符串切片是否为回文字符串
    for i in range(len(s)):
        for j in range(len(s)):
            if i == j:
                dp[i][j] = True     # 对角线上的元素坑定是相等的


    for i in range(len(s)):
        for j in range(i):
            if s[i] == s[j] :
                if i-j <= 2:    # 注意这里是i大于j,也就是i在前，j在后，如果元素的下标位置距离小于等于2，且i,j位置上的元素相等
                    dp[i][j] = True # 那么可以判定从j->i位置切片的字符串是回文字符串
                else:
                    dp[i][j] = dp[i-1][j+1] # 如果j->i的间距大于2，而且i,j位置的字符相等，那么从i->j之间的与字符串切片是否为元组，取决于j右侧(j+1)的元素和i左侧(i-1)的元素这两者间距之间是否是回文字符串
            else:
                dp[i][j] = False    # i和j位置上的元素不相等时，置为False

            if dp[i][j] and s[j:i+1]:   # dp[i][j]为True且字符串切片s[j:i+1]不为空，那么字符串切片就是回文字符串
                res.append(s[j:i+1])
    return res

if __name__ == '__main__':
    # main()
    res = dp_process()
    print(res)