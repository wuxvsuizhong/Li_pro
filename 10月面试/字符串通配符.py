'''
问题描述：在计算机中，通配符一种特殊语法，广泛应用于文件搜索、数据库、正则表达式等领域。现要求各位实现字符串通配符的算法。
要求：
实现如下2个通配符：
*：匹配0个或以上的字符（注：能被*和?匹配的字符仅由英文字母和数字0到9组成，下同）
？：匹配1个字符

注意：匹配时不区分大小写。

输入：
通配符表达式；
一组字符串。
输出：

返回不区分大小写的匹配结果，匹配成功输出true，匹配失败输出false
数据范围：字符串长度：1≤s≤100
进阶：时间复杂度：O(n^2)\O(n
2
 ) ，空间复杂度：O(n)\O(n)
输入描述：
先输入一个带有通配符的字符串，再输入一个需要匹配的字符串

输出描述：
返回不区分大小写的匹配结果，匹配成功输出true，匹配失败输出false

示例1
输入：
te?t*.*
txt12.xls
输出：
false

示例2
输入：
z
zz
输出：
false

示例3
输入：
pq
pppq
输出：
false

示例4
输入：
**Z
0QZz
输出：
true

示例5
输入：
?*Bc*?
abcd
输出：
true

示例6
输入：
h*?*a
h#a
输出：
false

说明：
根据题目描述可知能被*和?匹配的字符仅由英文字母和数字0到9组成，所以?不能匹配#，故输出false
示例7
输入：
p*p*qp**pq*p**p***ppq
pppppppqppqqppqppppqqqppqppqpqqqppqpqpppqpppqpqqqpqqp

输出：
false
'''
import sys

# 这个题目使用动态规划
pattern = input().strip().lower()
s = input().strip().lower()
special_ch='#@'
for sc in special_ch:
    if sc in s:
        print("false")
        sys.exit(0)

dp = [[False for _ in range(len(s)+1)] for _ in range(len(pattern)+1)]
for i in range(len(dp[0])):
    if i == 0:
        dp[0][i] = True
    else:
        dp[0][i] = False

for i in range(1,len(dp)):
    for j in range(len(dp[i])):
        if j > 0:
            if pattern[i-1] not in '?*':
                if pattern[i-1] == s[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = False
            elif pattern[i-1] == '?':
                dp[i][j] = dp[i-1][j-1]
            elif pattern[i-1] == '*':
                dp[i][j] = dp[i][j-1] or dp[i-1][j] or dp[i-1][j-1]
            else:
                pass
        else:
            if i > 0:
                if pattern[i-1] not in '?*':
                    dp[i][j] = False
                elif pattern[i-1]  == '?':
                    dp[i][j] = False
                elif pattern[i-1] == '*':
                    dp[i][j] = dp[i-1][j]


if dp[len(pattern)][len(s)]:
    print('true')
else:
    print('false')
