# 在一个数组中，一个数左边比它小的数的总和，叫数的小和，所有的数的小何累加起来，叫数组小和。
#给定一个数组吗，求其数组小和
# 例子：[1,3,4,2,5]
# 1左边比1小的数：无
# 3左边比3小的数：1
# 4坐标比4小的数：1,3
# 2左边比2小的数：1
# 5左边比5小的数：1,3,4,2
# 所以数组小和：1+1+3+1+1+3+4+2 = 16

li=[1,3,4,2,5]
li=[1, 78, 40, 30, 17, 39, 22, 77, 23, 85]


def merge(arr,l,m,r):
    print("l,m,r:",l,m,r)
    i,j = l,m+1
    tmp=[]
    res = 0
    while i<=m and j <= r:
        if arr[i] < arr[j]:
            res += (r-j+1)*arr[i]       # 这里需要理解，在计算某个数的小和的时候，原本是统计的是左侧小于该数的数据
            # 但是这里采用了反向的方式，统计左侧有多少个小于该数据的个数=>统计右侧大于该数据的个数
            tmp.append(arr[i])
            i += 1
        elif arr[i] >= arr[j]:
            tmp.append(arr[j])
            j += 1

    if i <= m:
        tmp.extend(arr[i:m+1])
    if j <= r:
        tmp.extend(arr[j:r+1])

    print("tmp:",tmp)
    for i,val in enumerate(tmp):
        arr[l+i] = val

    return res

def merge_sort(li,l,r):
    print("l,r:",l,r)
    if l == r:
        return 0
    mid = ((r-l)>>2)+l
    return merge_sort(li,l,mid) + merge_sort(li,mid+1,r) + merge(li,l,mid,r)

r = merge_sort(li,0,len(li)-1)
print('r:',r)
print(li)
print('-'*20)

# 找出一组数据中的逆序对
# 如对于数据 3,2,4,1,5 逆序对有3,2 3,1 2,1 4,1 ，使用逆向思维的方式，当一个数据是逆序对想x,y中的数据时，有x>y ，也就是在数组中，找出y左侧的所有的比y大的数据，然后分别构成逆序对。
# 问题就转化为了，求出数组中，对每个数而言，在数的左侧比该数据大的数据的个数；
# 按照归并排序在merge的时候的做法，左右组的数据，每次在合并的时候，左右的基准数据i,j.
def merge(arr,l,m,r):
    if l == r:
        return 0
    tmp = []
    cnt = 0
    i,j = l,m+1
    while i <=m and j <= r:
        if arr[i] <= arr[j]:
            tmp.append(arr[i])
            i += 1
        elif arr[i] > arr[j]:
            cnt += (m-i+1)
            tmp.append(arr[j])
            j += 1

    if i <= m:
        tmp.extend(arr[i:m+1])
    if j <= r:
        tmp.extend(arr[j:r+1])

    print(tmp)
    for i,val in enumerate(tmp):
        arr[i+l] = val

    return cnt

def merge_sort(li,l,r):
    if l == r:
        return 0
    mid = l + ((r-l)>>1)
    return merge_sort(li,l,mid) + merge_sort(li,mid+1,r) + merge(li,l,mid,r)

# li = [3,2,4,1,5]
li=[1, 78, 40, 30, 17, 39, 22, 77, 23, 85]
r = merge_sort(li,0,len(li)-1)
print('r:',r)
print(li)


