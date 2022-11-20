'''
给出一个仅包含字符'(',')','{','}','['和']',的字符串，判断给出的字符串是否是合法的括号序列
括号必须以正确的顺序关闭，"()"和"()[]{}"都是合法的括号序列，但"(]"和"([)]"不合法。

数据范围：字符串长度 100000≤n≤10000
要求：空间复杂度 O(n)O(n)，时间复杂度 O(n)O(n)
示例1
输入：
"["
返回值：
false

示例2
输入：
"[]"
返回值：
true
'''
def main():
    line = input().strip()
    stack = []
    opmap = {
        ")":"(",
        "]":"[",
        "}":"{",
    }
    for each in line:
        if each in '[({':
            stack.append(each)
        else:
            if each in '])}' and stack and stack[-1] == opmap[each]:
                stack.pop()
            else:
                print("false")

    if len(stack) > 0:
        print("false")
    else:
        print("true")


if __name__ == '__main__':
    main()