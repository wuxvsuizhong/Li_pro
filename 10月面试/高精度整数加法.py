'''
输入两个用字符串 str 表示的整数，求它们所表示的数之和。

数据范围：1≤len(str)≤10000
输入描述：
输入两个字符串。保证字符串只含有'0'~'9'字符

输出描述：
输出求和后的结果

示例1
输入：
9876543210
1234567890

输出：
11111111100
'''
n1_list = list(map(int,list(input().strip())))
n2_list = list(map(int,list(input().strip())))

print(n1_list,n2_list)
longnum,shortnum = n1_list,n2_list
if len(n1_list) < len(n2_list):
    longnum,shortnum = n2_list,n1_list

longnum.reverse()
shortnum.reverse()

for i,v in enumerate(shortnum):
    longnum[i] = v + longnum[i]

# print(longnum)
for i,v in enumerate(longnum):
    if v > 9:
        v -= 10
        longnum[i] = v
        if i+1 >= len(longnum):
            longnum.append(1)
        else:
            longnum[i+1] += 1

longnum.reverse()
print(''.join(list(map(str,longnum))))
