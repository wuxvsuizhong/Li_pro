"""
按照斜向的螺旋线轨迹打印数组

如，有如下矩阵，
[ 1, 2, 3, 4, 5, 6]
[ 7, 8, 9,10,11,12]
[13,14,15,16,17,18]
[19,20,21,22,23,24]
按照打印方式:
1,2,7,13,8,3,4,9,14,19,20,15,10,5,6,11,16,21,22,17,12,18,23,24

分析:矩阵打印，以更宏观的双指针，分别为横向的和纵向的指针，每次横向指针右移，纵向指针下移；
当横向指针移动到右边界的时候，再继续向下移动，当纵向指针移动到下边界的时候，转而向右，最终两个指针交汇于终点matrix[i][j]
"""
import dataclasses
import random

@dataclasses.dataclass
class Point:
    x:int
    y:int

    def __eq__(self, other):
        if isinstance(other,Point):
            if self.x == other.x and self.y == other.y:
                return True
        return False
    def __sub__(self, other):
        return Point(self.x - other.x,self.y-other.y)

def print_line(li:list,row_first:Point,col_first:Point,direction:str):
    # print(s,e,direction)
    # print(li[s.y][s.x],col_first=' ')
    while row_first != col_first:
        if direction == 'down':  # 从横向点向纵向点移动打印
            print(li[row_first.x][row_first.y], end=' ')
            tx,ty = 1,-1
            row_first = Point(row_first.x+tx,row_first.y+ty)
        else: # 从纵向点向横向点移动打印
            print(li[col_first.x][col_first.y], end=' ')
            tx,ty = -1,1
            col_first = Point(col_first.x+tx,col_first.y+ty)

    print(li[col_first.x][col_first.y])

def slant_print_matrix(li,direction):
    """斜向螺旋打印矩阵"""
    row_first,col_first = Point(0,0),Point(0,0)
    print_line(li,row_first,col_first,direction)
    row_first,col_first = Point(0,1),Point(1,0)
    while row_first != col_first:
        if direction == 'up':
            direction = 'down'
        else:
            direction = 'up'
        print_line(li,row_first,col_first,direction)

        if row_first.y < len(li[0])-1:
            row_first.y += 1
        else:
            row_first.x += 1
        if col_first.x < len(li)-1:
            col_first.x += 1
        else:
            col_first.y += 1
    print_line(li,row_first,col_first,direction)
#
# if __name__ == "__main__":
#     li = [[random.randint(0,100) for _ in range(10)] for _ in range(5)]
#     for each in li:
#         print(each)
#     slant_print_matrix(li,'down')


'''
数组的螺旋打印
如，有如下矩阵，
[ 1, 2, 3, 4, 5, 6]
[ 7, 8, 9,10,11,12]
[13,14,15,16,17,18]
[19,20,21,22,23,24]

顺时针螺旋打印：1,2,3,4,5,6,12,18,24,23,22,21,20,19,13,7,8,9,10,11,17...

解析:确定矩阵的点，matrix[0][0],matrix[0][5],matrix[3][5],natrix[3][0]
游标从[0][0]位置开始，先向右递增，到右上角，再向下递增，到右下角，向左递减，到左下角，向上递减。然后一圈结束；
一圈结束的位置就是下一圈开始的位置，然后重复上述过程。
可使用矩阵左上角坐标和右下角坐标，4个参数来圈定数据范围，并在遍历过程中向内缩这个范围
'''

def print_line2(li,lt_row,lt_col,rd_row,rd_col):
    if lt_row <= rd_row:
        # 为防止单列或者单行的时候，出现重复的打印，针对行打印时，打印完成后，行数自增1，也就是说只有判断lt_row和rd_row在不冲突的情况下才进行行的打印
        for i in range(lt_col,rd_col+1):
            print(li[lt_row][i],end=' ')
        lt_row += 1 # 行数移动1
        print()
    if lt_col <= rd_col:
        # 和上方的行数处理类似，在列处理完后，列数移动1，防止lt_col和rd_col冲突
        for i in range(lt_row,rd_row+1):
            print(li[i][rd_col],end=' ')
        rd_col -= 1 # 列数移动1
        print()

    if lt_row <= rd_row:
        for i in range(rd_col,lt_col-1,-1):
            print(li[rd_row][i],end=' ')
        rd_row -= 1
        print()

    if lt_col <= rd_col:
        for i in range(rd_row,lt_row-1,-1):
            print(li[i][lt_col],end=' ')
        lt_col +=1
        print()


def print_rect(li):
    """顺时针打印矩阵"""
    lt_row,lt_col = 0,0
    rd_row,rd_col = len(li)-1,len(li[0])-1

    while lt_row <= rd_row and lt_col <= rd_col:
        # print(lt_row,lt_col,rd_row,rd_col)
        print_line2(li,lt_row,lt_col,rd_row,rd_col)
        lt_row+=1
        lt_col+=1
        rd_row-=1
        rd_col-=1
        # print(lt_row,lt_col,rd_row,rd_col)


if __name__ == "__main__":
    li = [[random.randint(0,100) for _ in range(10)] for _ in range(5)]
    for each in li:
        print(each)
    print_rect(li)