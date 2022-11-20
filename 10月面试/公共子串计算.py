'''
给定两个只包含小写字母的字符串，计算两个字符串的最大公共子串的长度。

注：子串的定义指一个字符串删掉其部分前缀和后缀（也可以不删）后形成的字符串。
数据范围：字符串长度：1≤s≤150
进阶：时间复杂度：O(n^3)，空间复杂度：O(n)
输入描述：
输入两个只包含小写字母的字符串

输出描述：
输出一个整数，代表最大公共子串的长度

示例1
输入：
asdfas
werasdfaswer

输出：
6
'''
s1 = input().strip()
s2 = input().strip()

# 动态规划
dp = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
for i in range(len(s1[0])):
    dp[0][i] = 0
for i in range(len(dp)):
    dp[i][0] = 0

maxval = 0
pos_node=[0,0]
for i in range(1, len(s1)+1):
    for j in range(1, len(s2)+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
            if dp[i][j] > maxval:
                maxval = dp[i][j]
                pos_node[0],pos_node[1] = i,j
        else:
            dp[i][j] = 0

print(maxval)

