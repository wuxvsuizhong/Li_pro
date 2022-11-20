'''
将一个字符串str的内容颠倒过来，并输出。

数据范围：1≤len(str)≤10000
输入描述：
输入一个字符串，可以有空格
示例1
输入：
I am a student
输出：
tneduts a ma I

示例2
输入：
nowcoder
输出：
redocwon
'''
import sys

def main():
    line = list(sys.stdin.readline().strip())
    start,end = 0,len(line)-1

    while start < end:
        line[start],line[end] = line[end],line[start]
        start += 1
        end -= 1

    print(''.join(line))


if __name__ == '__main__':
    main()