'''
在给定的m x n网格grid中，每个单元格可以有以下三个值之一：

值0代表空单元格；
值1代表新鲜橘子；
值2代表腐烂的橘子。
每分钟，腐烂的橘子周围4个方向上相邻的新鲜橘子都会腐烂。

返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回-1。

示例 1：
[2,1,1] -> 	[2,2,1]	->	[2,2,2]	->	[2,2,2]
[1,1,0]		[2,1,0]		[2,2,0]		[2,2,0]
[0,1,1]		[0,1,1]		[0,1,1]		[0,2,2]


输入：grid = [[2,1,1],[1,1,0],[0,1,1]]
输出：4

示例 2：
输入：grid = [[2,1,1],[0,1,1],[1,0,1]]
输出：-1
解释：左下角的橘子（第 2 行， 第 0 列）永远不会腐烂，因为腐烂只会发生在 4 个正向上。

示例 3：
输入：grid = [[0,2]]
输出：0
解释：因为 0 分钟时已经没有新鲜橘子了，所以答案就是 0 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/rotting-oranges
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
'''
def main():
    #BFS + 双队列
    grid = []
    while True:
        line = input().strip().split()
        if line:
            grid.append(line)
        else:
            break

    grid_rec = [[0 for _ in range(len(grid[j]))] for j in range(len(grid))]
    print(grid_rec)
    queue = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '2':
                grid_rec[i][j] = 1
                queue.append((i,j))

    directions = [
        [1,0],
        [-1,0],
        [0,-1],
        [0,1],
    ]

    quque2 = []
    cnt = 0

    while queue or quque2:
        flag = False
        while queue:
            x,y = queue.pop(0)
            for d in directions:
                tx,ty = x+d[0],y+d[1]

                if tx < 0 or tx >= len(grid) or ty < 0 or ty >= len(grid[x]):
                    continue

                print(tx,ty)
                if grid[tx][ty] == '1' and grid_rec[tx][ty] == 0:
                    flag = True
                    grid_rec[tx][ty] = 1
                    quque2.append((tx,ty))
                    grid[tx][ty] = '2'
        if flag:
            cnt += 1
        queue,quque2 = quque2,queue

    has_fresh=False
    for each in grid:
        if '1' in each:
            has_fresh = True
            break


    # print(grid)
    if has_fresh:
        print("-1")
    else:
        print(cnt)


if __name__ == '__main__':
    main()