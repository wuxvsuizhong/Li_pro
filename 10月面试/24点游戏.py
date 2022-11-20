'''
给出4个1-10的数字，通过加减乘除运算，得到数字为24就算胜利,除法指实数除法运算,运算符仅允许出现在两个数字之间,本题对数字选取顺序无要求，但每个数字仅允许使用一次，且需考虑括号运算
此题允许数字重复，如3 3 4 4为合法输入，此输入一共有两个3，但是每个数字只允许使用一次，则运算过程中两个3都被选取并进行对应的计算操作。
输入描述：
读入4个[1,10]的整数，数字允许重复，测试用例保证无异常数字。

输出描述：
对于每组案例，输出一行表示能否得到24点，能输出true，不能输出false

示例1
输入：
7 2 1 10
输出：
true
'''
import copy
nums = list(map(int,input().strip().split()))
options = ['+','-','*','/']
options.extend(nums)

book = [False for _ in range(len(options))]
calc_strs = []
def dfs(calc_list,f_quantity):
    calc_list_len = len(calc_list)
    if calc_list_len == 7:
        calc_strs.append(copy.copy(calc_list))
        return

    for i,op in enumerate(options):
        if 3 < i < len(options) and not book[i]:
            #未使用的数字
            book[i] = True
            calc_list.append(op)
            dfs(calc_list,f_quantity)
            calc_list.pop()
            book[i] = False
        elif 3 < i < len(options) and book[i]:
            continue
        else:
            if calc_list_len < 2:
                continue
            if f_quantity+1 < 4:
                calc_list.append(op)
                dfs(calc_list,f_quantity+1)
                calc_list.pop()
            else:
                continue

dfs([],0)
# print(calc_strs)

def calc_str(slist):
    stack = []
    for each in slist:
        if str(each) not in '+-*/':
            stack.append(each)
        else:
            if len(stack) == 2:
                n2,n1 = stack.pop(),stack.pop()
            else:
                return 0
            if each == '+':
                stack.append(n1+n2)
            elif each == '-':
                stack.append(n1-n2)
            elif each == '/':
                stack.append(n1/n2)
            else:
                stack.append(n1*n2)
    # print(stack[0])
    return stack[0]

def calc_all():
    for each in calc_strs:
        if calc_str(each) == 24:
            print("true")
            return
    print('false')

calc_all()