'''
编写一个函数，计算字符串中含有的不同字符的个数。字符在 ASCII 码范围内( 0~127 ，包括 0 和 127 )，换行表示结束符，不算在字符里。不在范围内的不作统计。多个相同的字符只计算一次
例如，对于字符串 abaca 而言，有 a、b、c 三种不同的字符，因此输出 3 。

示例1
输入：
abc
输出：
3

示例2
输入：
aaa
输出：
1
'''
import sys


def main():
    s = sys.stdin.readline().strip()
    rec = {}
    for c in s:
        rec[c] = 1 if c not in rec else rec[c] + 1

    print(len(rec.keys()))


if __name__ == '__main__':
    main()
