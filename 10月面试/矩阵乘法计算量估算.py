'''
矩阵乘法的运算量与矩阵乘法的顺序强相关。
例如：

A是一个50×10的矩阵，B是10×20的矩阵，C是20×5的矩阵

计算A*B*C有两种顺序：((AB)C)或者(A(BC))，前者需要计算15000次乘法，后者只需要3500次。

编写程序计算不同的计算顺序需要进行的乘法次数。

数据范围：矩阵个数：1≤n≤15 ，行列数：1≤rowi ,coli ≤100 ，保证给出的字符串表示的计算顺序唯一。
进阶：时间复杂度：O(n)\O(n) ，空间复杂度：O(n)\O(n)

输入描述：
输入多行，先输入要计算乘法的矩阵个数n，每个矩阵的行数，列数，总共2n的数，最后输入要计算的法则
计算的法则为一个字符串，仅由左右括号和大写字母（'A'~'Z'）组成，保证括号是匹配的且输入合法！

输出描述：
输出需要进行的乘法次数

示例1
输入：
3
50 10
10 20
20 5
(A(BC))

输出：
3500
'''

def calc_times_count(m1,m2):
    row_m1 = m1[0]
    col_m1 = m1[1]
    col_m2 = m2[1]
    return row_m1*col_m2*col_m1,row_m1,col_m2

quantity = int(input().strip())
matrix_info = []
for i in range(quantity):
    line = list(map(int,input().strip().split()))
    matrix_info.append(line)

# print(matrix_info)
rule = input().strip()
index_map = {}
for x in range(ord('A'),ord('Z')):
    index_map[chr(x)] = x-ord('A')

stack = []
sum = 0
for c in rule:
    if c == '(':
        stack.append(c)
    elif c == ')':
        tmp_list=[]
        while stack and stack[-1] != '(':
            # m2,m1 = stack.pop(),stack.pop()
            tmp_list.append(stack.pop())
        # print('tmp_list',tmp_list)
        if stack and stack[-1] == '(':
            stack.pop()
        if tmp_list and len(tmp_list)  == 2:
            m2,m1 = tmp_list[0],tmp_list[1]
            result,row,col = calc_times_count(m1,m2)
            # print('result,',result)
            sum += result
            stack.append([row,col])
        else:
            stack.append(tmp_list[0])
    else:
        if stack and stack[-1] != '(':
            r = stack.pop()
            index = index_map[c]
            result, row, col = calc_times_count(r,matrix_info[index])
            # print('result,', result)
            sum += result
            stack.append([row, col])
        else:
            index = index_map[c]
            m = matrix_info[index]
            stack.append(m)
# print(stack)

print(sum)





