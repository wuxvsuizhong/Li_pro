'''
Levenshtein 距离，又称编辑距离，指的是两个字符串之间，由一个转换成另一个所需的最少编辑操作次数。许可的编辑操作包括将一个字符替换成另一个字符，插入一个字符，删除一个字符。编辑距离的算法是首先由俄国科学家 Levenshtein 提出的，故又叫 Levenshtein Distance 。

例如：
字符串A: abcdefg
字符串B: abcdef
通过增加或是删掉字符 ”g” 的方式达到目的。这两种方案都需要一次操作。把这个操作所需要的次数定义为两个字符串的距离。
要求：

给定任意两个字符串，写出一个算法计算它们的编辑距离。
数据范围：给定的字符串长度满足1≤len(str)≤1000
输入描述：
每组用例一共2行，为输入的两个字符串
输出描述：
每组用例输出一行，代表字符串的距离

示例1
输入：
abcdefg
abcdef

输出：
1
'''
l1 = input().strip()
l2 = input().strip()

# l1->l2
dp = [[0 for _ in range(len(l2)+1)] for _ in range(len(l1)+1)]
for i in range(len(dp)):
    for j in range(len(dp[i])):
        if i == 0:
            dp[i][j] = j
        if j == 0:
            dp[i][j] = i
        if i > 0 and j > 0:
            if l1[i-1] != l2[j-1]:
                dp[i][j] =min(dp[i][j-1],dp[i-1][j-1],dp[i-1][j])+1
            else:
                dp[i][j] = dp[i-1][j-1]

print(dp[len(l1)][len(l2)])

