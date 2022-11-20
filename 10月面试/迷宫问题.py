'''
定义一个二维数组 N*M ，如 5 × 5 数组下所示：
int maze[5][5] = {
0, 1, 0, 0, 0,
0, 1, 1, 1, 0,
0, 0, 0, 0, 0,
0, 1, 1, 1, 0,
0, 0, 0, 1, 0,
};

它表示一个迷宫，其中的1表示墙壁，0表示可以走的路，只能横着走或竖着走，不能斜着走，要求编程序找出从左上角到右下角的路线。入口点为[0,0],既第一格是可以走的路。

数据范围：2≤n,m≤10  ， 输入的内容只包含0≤val≤1

输入描述：
输入两个整数，分别表示二维数组的行数，列数。再输入相应的数组，其中的1表示墙壁，0表示可以走的路。数据保证有唯一解,不考虑有多解的情况，即迷宫只有一条通道。

输出描述：
左上角到右下角的最短路径，格式如样例所示。

示例1
输入：
5 5
0 1 0 0 0
0 1 1 1 0
0 0 0 0 0
0 1 1 1 0
0 0 0 1 0

输出：
(0,0)
(1,0)
(2,0)
(2,1)
(2,2)
(2,3)
(2,4)
(3,4)
(4,4)

示例2
输入：
5 5
0 1 0 0 0
0 1 0 1 0
0 0 0 0 1
0 1 1 1 0
0 0 0 0 0

输出：
(0,0)
(1,0)
(2,0)
(3,0)
(4,0)
(4,1)
(4,2)
(4,3)
(4,4)

说明：
注意：不能斜着走！！
'''
height,wide = map(int,input().strip().split())
square = []
for i in range(height):
    square.append(list(map(int,input().strip().split())))

directoins = [
    [1,0],
    [-1,0],
    [0,-1],
    [0,1],
]

queue = []
queue.append(((0,0),(0,0)))

book = [[0 for _ in range(wide)] for _ in range(height)]
for i in range(height):
    for j in range(len(square[i])):
        if square[i][j] == 1:
            book[i][j] = 1
book[0][0]=-1

path_stack = []
is_arrive = False
while queue:
    p = queue.pop(0)
    path_stack.append(p)
    x,y,p_x,p_y = p[0][0],p[0][1],p[1][0],p[1][1]
    book[x][y] = -1

    for d in directoins:
        tx,ty = x+d[0],y+d[1]
        if tx == height - 1 and ty == wide - 1:
            is_arrive = True
            path_stack.append(((tx, ty), (x, y)))
            break
        if tx < 0 or tx >= height or ty < 0 or ty >= wide:
            continue
        if square[tx][ty] != 1 and book[tx][ty] != -1:
            queue.append(((tx,ty),(x,y)))
    if is_arrive:
        break
#
# print(book)
c_list = [x[0] for x in path_stack]
p_list = [x[1] for x in path_stack]

res=[]
target_list=c_list
node = (height-1,wide-1)
res.append((node))
while node != (0,0):
    index = target_list.index(node)
    res.append(p_list[index])
    node = p_list[index]
    target_list = c_list

res.reverse()
for each in res:
    print(str(each).replace(' ',''))

