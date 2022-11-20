'''
编写一个程序，将输入字符串中的字符按如下规则排序。
规则 1 ：英文字母从 A 到 Z 排列，不区分大小写。
如，输入： Type 输出： epTy

规则 2 ：同一个英文字母的大小写同时存在时，按照输入顺序排列。
如，输入： BabA 输出： aABb

规则 3 ：非英文字母的其它字符保持原来的位置。
如，输入： By?e 输出： Be?y

数据范围：输入的字符串长度满足1≤n≤1000

输入描述：
输入字符串
输出描述：
输出字符串
示例1
输入：
A Famous Saying: Much Ado About Nothing (2012/8).
输出：
A aaAAbc dFgghh: iimM nNn oooos Sttuuuy (2012/8).
'''
l = input().strip()
rec_map={}
for i,c in enumerate(l):
    if not c.isalpha():
        rec_map[i] = c

alphas = [x.lower() for x in l if x.isalpha()]
alphas.sort()

def search_ch(c,s):
    res = []
    for e in s:
        if e == c or abs(ord(e)-ord(c)) == 32:
            res.append(e)
    return res

i=0
while i<len(alphas):
    ret = search_ch(alphas[i],l)
    alphas = alphas[:i] + ret + alphas[i+len(ret):]
    i += len(ret)

for k,v in rec_map.items():
    alphas.insert(k,v)
print(''.join(alphas))


