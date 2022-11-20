'''
描述
给定 n 个字符串，请对 n 个字符串按照字典序排列。

数据范围：1≤n≤1000  ，字符串长度满足 100 \1≤len≤100
输入描述：
输入第一行为一个正整数n(1≤n≤1000),下面n行为n个字符串(字符串长度≤100),字符串中只含有大小写字母。
输出描述：
数据输出n行，输出结果为按照字典序排列的字符串。

示例1
输入：
9
cap
to
cat
card
two
too
up
boat
boot

输出：
boat
boot
cap
card
cat
to
too
two
up
'''
def main():
    quantity = int(input().strip())
    chars=[]
    for i in range(quantity):
        chars.append(input().strip())

    for i in range(1,quantity):
        for j in range(quantity-i):
            if chars[j] > chars[j+1]:
                chars[j],chars[j+1] = chars[j+1],chars[j]
    for each in chars:
        print(each)


if __name__ == '__main__':
    main()