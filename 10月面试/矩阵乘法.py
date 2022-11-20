'''
如果A是个x行y列的矩阵，B是个y行z列的矩阵，把A和B相乘，其结果将是另一个x行z列的矩阵C。这个矩阵的每个元素是由下面的公式决定的

矩阵的大小不超过100*100
输入描述：
第一行包含一个正整数x，代表第一个矩阵的行数
第二行包含一个正整数y，代表第一个矩阵的列数和第二个矩阵的行数
第三行包含一个正整数z，代表第二个矩阵的列数
之后x行，每行y个整数，代表第一个矩阵的值
之后y行，每行z个整数，代表第二个矩阵的值

输出描述：
对于每组输入数据，输出x行，每行z个整数，代表两个矩阵相乘的结果
示例1
输入：
2
3
2
1 2 3
3 2 1
1 2
2 1
3 3

输出：
14 13
10 11

说明：
1 2 3
3 2 1
乘以
1 2
2 1
3 3
等于
14 13
10 11
'''
row = int(input().strip())
col = int(input().strip())
row2 = int(input().strip())
matrix1 = []
matrix2 = []
for i in range(row):
    matrix1.append(list(map(int,input().strip().split())) )

for i in range(col):
    matrix2.append(list(map(int,input().strip().split())) )

# print(matrix1)
# print(matrix2)

def calc_list(l1,l2):
    # print("l1:",l1)
    # print("l2:",l2)
    return sum([l1[i]*l2[i] for i in range(len(l1))])

def calc_matrix(m1,m2):
    res_matrix =[]
    for i in range(len(m1)):
        tmp_res_list=[]
        col = []
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                # print("k,j",k,j)
                col.append(m2[k][j])
            # print(m1[i],col)
            ret = calc_list(m1[i],col)
            col.clear()
            # print(ret)
            tmp_res_list.append(ret)
        res_matrix.append(tmp_res_list)
    return res_matrix   

mat_ret = calc_matrix(matrix1,matrix2)
for i in range(len(mat_ret)):
    for j in range(len(mat_ret[i])):
        print(mat_ret[i][j],end= ' ')
    print()


