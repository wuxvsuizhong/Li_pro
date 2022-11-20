'''
给出一个字符串，该字符串仅由小写字母组成，定义这个字符串的“漂亮度”是其所有字母“漂亮度”的总和。
每个字母都有一个“漂亮度”，范围在1到26之间。没有任何两个不同字母拥有相同的“漂亮度”。字母忽略大小写。

给出多个字符串，计算每个字符串最大可能的“漂亮度”。

本题含有多组数据。

数据范围：输入的名字长度满足1≤n≤10000

输入描述：
第一行一个整数N，接下来N行每行一个字符串

输出描述：
每个字符串可能的最大漂亮程度

示例1
输入：
2
zhangsan
lisi

输出：
192
101

说明：
对于样例lisi，让i的漂亮度为26，l的漂亮度为25，s的漂亮度为24，lisi的漂亮度为25+26+24+26=101.
'''
quantity = int(input().strip())
lines = []
for i in range(quantity):
    lines.append(input().strip())


res = []
for l in lines:
    rec_map = {}
    for c in l:
        if c in rec_map:
            rec_map[c] += 1
        else:
            rec_map[c] = 1

    res.append(rec_map)

result = []
for each in res:
    tmp_r = list(zip(each.values(),each.keys()))
    tmp_r.sort(reverse=True)
    result.append(tmp_r)
# print(result)

for itms in result:
    sumval=0
    for i in range(26,26-len(itms),-1):
        sumval += i*itms[26-i][0]
    print(sumval)


