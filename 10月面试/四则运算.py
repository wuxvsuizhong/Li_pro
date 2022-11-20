'''
输入一个表达式（用字符串表示），求这个表达式的值。
保证字符串中的有效字符包括[‘0’-‘9’],‘+’,‘-’, ‘*’,‘/’ ,‘(’， ‘)’,‘[’, ‘]’,‘{’ ,‘}’。且表达式一定合法。

数据范围：表达式计算结果和过程中满足 |val|≤1000  ，字符串长度满足1≤n≤1000

输入描述：
输入一个算术表达式

输出描述：
得到计算结果

示例1
输入：
3+2*{1+2*[-4/(8-6)+7]}
输出：
25
'''

line = input().strip()
ret = []
def split_val(s):
    if not s:
        return

    if s[0].isdigit() and ret and ret[-1].isdigit():
        # ret.append(s[0])
        ret[-1] += s[0]
        split_val(s[1:])
    elif s[0] == '-' and ret[-1] in '[{(':
        ret.append(s[:2])
        split_val(s[2:])
    else:
        ret.append(s[0])
        split_val(s[1:])

split_val(line)

#中缀转后缀
oplev_map={
    '+':1,
    '-':1,
    '*':2,
    '/':2,
    '(':0,
    '{':0,
    '[':0,
}

op_grp = {
    ')':'(',
    ']':'[',
    '}':'{',
}

op_stack = []
res=[]
for c in ret:
    if c.isdigit():
        res.append(c)
    elif len(c) > 1 and c[0] == '-':
        res.append(c)
    elif not op_stack or c in '{[(':
        op_stack.append(c)
    elif c in ')]}':
        while True:
            r = op_stack.pop()
            if r == op_grp[c]:break
            res.append(r)
    else:
        if oplev_map[op_stack[-1]] < oplev_map[c]:
            # 字符串中操作符优先级高于op_stack 栈顶，直接入栈
            op_stack.append(c)
        else:# 字符串中的优先级小于op_stack 栈顶，栈一致出直到字符串操作符的优先级能够大于栈顶，然后字符串操作符再入栈
            print(res)
            print(op_stack)
            while op_stack and  oplev_map[op_stack[-1]] >= oplev_map[c]:
                res.append(op_stack.pop())
            op_stack.append(c)

while op_stack:
    res.append(op_stack.pop())

print(res)

num_stack= []
for each in res:
    if each not in '+-*/':
        num_stack.append(int(each))
    else:
        n2, n1 = num_stack.pop(), num_stack.pop()
        if each == '+':
            num_stack.append(n1+n2)
        elif each == '-':
            num_stack.append(n1 - n2)
        elif each == '*':
            num_stack.append(n1*n2)
        else:
            num_stack.append(n1/n2)

    print(num_stack)

print(int(num_stack[0]))


