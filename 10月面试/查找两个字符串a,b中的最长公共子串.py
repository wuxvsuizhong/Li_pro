'''
查找两个字符串a,b中的最长公共子串。若有多个，输出在较短串中最先出现的那个。
注：子串的定义：将一个字符串删去前缀和后缀（也可以不删）形成的字符串。请和“子序列”的概念分开！

数据范围：字符串长度1≤length≤300
进阶：时间复杂度：O(n^3)\O(n^3) ，空间复杂度：O(n)\O(n)
输入描述：
输入两个字符串

输出描述：
返回重复出现的字符
示例1
输入：
abcdefghijklmnop
abcsafjklmnopqrstuvw
输出：
jklmnop
'''

s1 = input().strip()
s2 = input().strip()

dp = [[0 for j in range(len(s1)+1)] for i in range(len(s2)+1)]

maxval = 0
x,y = 0,0
res = []
for i in range(1,len(s2)+1):
    for j in range(1,len(s1)+1):
        if s2[i-1] == s1[j-1]:
            dp[i][j] = dp[i-1][j-1]+1
            if dp[i][j] > maxval:
                maxval = dp[i][j]
                x,y = i,j
                res.clear()
                res.append((maxval,x,y))
            elif dp[i][j] == maxval and (i,j) != (x,y):
                maxval = dp[i][j]
                x, y = i, j
                res.append((maxval, x, y))
        else:
            dp[i][j] = 0

res.sort()
# print(res)

mlen = res[0][0]
if len(s1) < len(s2):
    mval = len(s2)
    for i in range(len(res)):
        if res[i][2] < mval:
            mval = res[i][2]
    print(s1[mval-mlen:mval])
else:
    mval = len(s1)
    for i in range(len(res)):
        if res[i][1] < mval:
            mval = res[i][1]
    # print(mval)
    print(s2[mval-mlen:mval])




# print(s2[x-maxval:x])



