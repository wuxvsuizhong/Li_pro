'''
实现删除字符串中出现次数最少的字符，若出现次数最少的字符有多个，则把出现次数最少的字符都删除。输出删除这些单词后的字符串，字符串中其它字符保持原来的顺序。
数据范围：输入的字符串长度满足 1≤n≤20  ，保证输入的字符串中仅出现小写字母
输入描述：
字符串只包含小写英文字母, 不考虑非法输入，输入的字符串长度小于等于20个字节。
输出描述：
删除字符串中出现次数最少的字符后的字符串

示例1
输入：
aabcddd
输出：
aaddd
'''
import sys
import re

def main():
    lines = []
    while True:
        line = sys.stdin.readline().strip()
        if line:
            lines.append(line)
        else:
            break

    result = []
    for l in lines:
        rec = {}
        for c in l:
            rec[c] = 1 if c not in rec else rec[c]+1

        itms = list(zip(rec.values(),rec.keys()))
        itms.sort()
        # print(itms)
        needmove=''
        prevcount = itms[0][0]
        for count,ch in itms:
            if count == prevcount:
                needmove += ch

        result.append(re.sub('[{}]'.format(needmove),'',l))

    for each in result:
        print(each)

if __name__ == '__main__':
    main()


