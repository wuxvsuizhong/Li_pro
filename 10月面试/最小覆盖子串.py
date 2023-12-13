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

import copy
def main1():
    chars = input().strip().split()
    s = chars[0]
    pattern = chars[1]

    rec = {}
    for i,v in enumerate(s):
        if v not in pattern:
            continue
        if v not in rec:
            rec[v] = [i]
        else:
            rec[v].append(i)

    res = list(rec.values())
    print(res)

    result = []
    opmap = copy.copy(res)
    def dfs(grp):
        # print(grp)
        if len(grp) == len(pattern):
            result.append(copy.copy(grp))
            return

        for i in range(len(res)):
            if -1 in res[i]:  # 剪枝，对于同组的res元组(是一个分组),只要有一个被选中即可)
                return
            for j in range(len(res[i])):
                if opmap[i][j] != -1:  # 判断元素是否被访问过
                    oldv = opmap[i][j]  # 备份一下元素的初始值
                    grp.append(res[i][j])   # 抽取元素添加到分组中
                    opmap[i][j] = -1    # 这里是对防访问过的元素设置访问标记，子啊一次循环的时候不再参与循环
                    dfs(grp)    # 递归调用dfs
                    grp.pop()   # dfs调用地柜调用返回后，恢复grp中的原来的值
                    opmap[i][j] = oldv # 恢复现场
    dfs([])
    print('result:',result)
    # 排序result
    for i in range(len(result)):
        result[i].sort()
        result[i] = [result[i][0],result[i][-1]]
    # print(result)
    minitm = result[0]
    for each in result:
        if each[1]-each[0] < minitm[1]-minitm[0]:
            minitm = each

    if minitm[1] == len(s)-1:
        minitm[1] = -1
    else:
        minitm[1]
    # print(minitm)
    b,e = minitm[0],minitm[1]
    print(s[b:e]+s[e])

    # 实际上不需要对result进行排序，只需要选出最大值和最小值即可
    # subidxs = ([min(each), max(each)] for each in result)

def main():
    chars = input().strip().split()
    s = chars[0]
    pattern = chars[1]

    if len(pattern) > len(s):
        print("")

    patt = pattern
    res = []
    stack = []
    for i,c in enumerate(s):
        if c in pattern:
            stack.append(i)
    print(stack)

    while stack:
        pos = stack.pop(0)
        start, end = pos, pos
        patt = pattern
        for i in range(pos,len(s)):
            patt = patt.replace(s[i],'',1)
            if len(patt) == 0:
                end = i
                if end - start + 1 >= len(pattern):
                    res.append([start,end])
                break

    print(res)
    if not res:
        return ""

    itm = res[0]
    for item in res:
        if item[1] - item[0] < itm[1] - itm[0]:
            itm = item
    l,r = itm
    print(s[l:r]+s[r])

if __name__ == '__main__':
    # main()
    main1()