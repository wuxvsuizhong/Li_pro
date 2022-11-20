'''
给出两个字符串 s 和 t，要求在 s 中找出最短的包含 t 中所有字符的连续子串。

数据范围：0≤∣S∣,∣T∣≤10000，保证s和t字符串中仅包含大小写英文字母
要求：进阶：空间复杂度 O(n)O(n) ， 时间复杂度 O(n)O(n)
例如：
S ="XDOYEZODEYXNZ"
T ="XYZ"
找出的最短子串为"YXNZ""YXNZ".

注意：
如果 s 中没有包含 t 中所有字符的子串，返回空字符串 “”；
满足条件的子串可能有很多，但是题目保证满足条件的最短的子串唯一。

示例1
输入：
"XDOYEZODEYXNZ","XYZ"
返回值：
"YXNZ"
示例2
输入：
"abcAbA","AA"
返回值：
"AbA"
'''

s,pattern = input().strip().split()
rec_map={}
for c in pattern:
    rec_map[c] = 1 if c not in rec_map else rec_map[c]+1
res = []

# print(rec_map)
rec_map_cp = rec_map.copy()
start,end = -1,-1
cnt = 0
for i,c in enumerate(s):
    if c in rec_map:
        if start == -1:
            start = i
            end = i
        else:
            end = i
        if rec_map[c] > 0:
            rec_map[c] -= 1
        for val in rec_map.values():
            if val == 0:
                cnt += 1
        if cnt == len(rec_map):
            print()
            res.append(s[start:end]+s[end])
            start,end = -1,-1
            rec_map = rec_map_cp.copy()

        cnt=0

# print(res)
if len(res) == 1:
    print(res[0])
else:
    minindex = 0
    for i,each in enumerate(res):
        if len(each) < len(res[minindex]):
            minindex = i
    print(res[minindex])



