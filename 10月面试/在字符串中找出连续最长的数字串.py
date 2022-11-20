'''
输入一个字符串，返回其最长的数字子串，以及其长度。若有多个最长的数字子串，则将它们全部输出（按原字符串的相对位置）
本题含有多组样例输入。

数据范围：字符串长度 1 \le n \le 200 \1≤n≤200  ， 保证每组输入都至少含有一个数字
输入描述：
输入一个字符串。1<=len(字符串)<=200

输出描述：
输出字符串中最长的数字字符串和它的长度，中间用逗号间隔。如果有相同长度的串，则要一块儿输出（中间不要输出空格）。

示例1
输入：
abcd12345ed125ss123058789
a8a72a6a5yy98y65ee1r2

输出：
123058789,9
729865,2

说明：
样例一最长的数字子串为123058789，长度为9
样例二最长的数字子串有72,98,65，长度都为2
'''
import sys

lines = []
while True:
    l = sys.stdin.readline().strip()
    if l:
        lines.append(l)
    else:
        break

res = []
for s in lines:
    start,end=-1,-1
    for i,c in enumerate(s):
        if c.isdigit():
            # print("i,isdig",i)
            if start == end and start == -1:
                start = i
                end = i
            else:
                end = i
        else:
            # print("{},not dig,start {},end {}".format(i,start,end))
            if start != -1:
                end = i
                # print("start,end,",start,end)
                # print(s[start:end])
                res.append(s[start:end])
                start,end = -1,-1


    if start != -1:
        # print(s[start:end]+s[-1])
        res.append(s[start:end]+s[-1])
    len_rec = [len(x) for x in res]
    len_rec.sort()
    maxpos=0
    for i,each in enumerate(len_rec):
        if each > len_rec[maxpos]:
            maxpos = i
    # print(len_rec[maxpos])
    maxlen = len_rec[maxpos]
    for each in res:
        if(len(each) == maxlen):
            print(each,end='')
    print(',{}'.format(maxlen))

    res.clear()



