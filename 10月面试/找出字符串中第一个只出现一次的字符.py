'''
找出字符串中第一个只出现一次的字符

数据范围：输入的字符串长度满足 1 \le n \le 1000 \1≤n≤1000

输入描述：
输入一个非空字符串

输出描述：
输出第一个只出现一次的字符，如果不存在输出-1

示例1
输入：
asdfasdfo

输出：
o
'''
import sys

s = input().strip()
if len(s) == 1:
    print(s)
    sys.exit(0)
rec_map={}
for i,c in enumerate(s):
    if c in rec_map:
        rec_map[c] += 1
    else:
        rec_map[c] = 1

itms = [itm for itm in rec_map.items() if itm[1] == 1]
if not itms:
    print('-1')
    sys.exit(0)

min_index = len(s)+1
# print(itms)
for val,cnt in itms:
    min_index = min(min_index,s.index(val))
    # print(min_index)

print(s[min_index])

