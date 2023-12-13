# partition过程
"""
给定一个数组arr,和一个整数num,请把小于等于num的数放在数组的左边，大于num的数放在数组的右边
算法的逻辑：从数组左边开始，从下标标序号0位置左侧，虚拟一位数据位-1，作为小于等于num的区域，记为l。
从数组的左侧开始，用num和数组的数据开始比较，如果数组下标index的数据<=num.那么把<=num区域的l的下一位，也就是l+1位置的数据和index交换位置，然后index+1做右移，因为此时l区域已经扩展了，所以l+=1,右扩一位。
如果当前数index>num，那么直接index+1向右移动一位，但是l保持不变
如数组li=[5,3,7,2,3,4,1] ,num=3
以li的0位置左侧虚拟一位-1，作为l=-1,然后index=0, li[index]>num ，index直接加一，此时index=1
li[index] == num,满足index<=num的条件，于是交换l+1位置的数据和index的数据，li[0],li[1] = li[1],li[0]，然后l+=1右移，l=0
此时li=[3,5,7,2,3,4,1], 此时index=1，l=0, index右移以为inde+=1 = 2，此时li[index]>num.index继续右移，index+=1 = 3
此时li[3]<num.于是交换index位置的数据和l+1位置的数据,此时l在0位置，于是li[3],li[1] = li[1],li[3],然后index右移index+=1 = 4
li=[3,2,7,5,3,4,1],l+=1右移,l=1，此时index=4，li[index]<= num.于是 l+1 = 2位置的数和index交换，li[4],li[2]=li[2],li[4]
li=[3,2,3,5,7,4,1],然后l向右扩1，l+=1=2, index继续向右index+=1=5, li[5]=4>num,index再向右，index=6,li[6]<num，交换index和l+1位置的数，li[6],li[3] = li[3],li[6],此时，li=[3,2,3,1,7,4,5] 而index已经触及到了li的边界，循环结束
循环完成后，l停留的位置就是分解位置，l左侧的所有数据都是小于num的，l右侧的数据都是大于num的

总结：整个的partition的过程就是不断地把左侧<=num的区域不断右扩的过程
"""
import random

# 荷兰国旗问题
"""
在partation问题上，扩展了==num的逻辑
给定一个数组arr,和一个整数num,要求<num的数据放做左边，=num的数据放中间，>num的数据放右边
算法逻辑：划分arr左侧从-1开始为虚拟的<num的左边界位l,同时划分数组arr右侧len(arr}位置开始为>num的右边界r
迭代arr的下标为index的数据，如果arr[index]<num,那么交换l+1和index位置的数据，然后index右扩1，同时l右扩1
如果index==num.那么直接index直接右扩index+=1即可，l和r不变
如果index>num,那么交换index和r-1位置的元素，然后右边界r-=1 向左扩1，但是此时index保持不变，因为从r-1的位置换到index位置的数据此时还内有参与比较，所以index此时不用右移，后面参与和num的比较

当index的位置和右侧r的边界相遇时，整个划分过程停止，也就循环条件index<r,当该条件不满足时，划分停止

总结：荷兰国旗为题就是在原来partition的基础上，多了右边界的操作，就是左边界向右扩展，右边界向左扩展的过程
"""

li=[3,5,4,0,4,6,7,2]
num = 4
def landsort(li,num):
    """荷兰国旗排序问题"""
    l,r = -1,len(li)
    index = 0
    while index<r:
        if l >= r:
            break
        if li[index] < num:
            print(f'change:{li[index]},{li[l+1]}')
            li[index],li[l+1] = li[l+1],li[index]
            l += 1
            index += 1  # 在index<num时，交换后，index右移
        elif li[index] > num:
            print(f'change:{li[index]},{li[r-1]}')
            li[index],li[r-1] = li[r-1],li[index]
            r -= 1  # 当index>num时，交换后，index暂时不右移
        else:
            index += 1 #当index==num时，index右移
        print(li)

# landsort(li,4)

# 引出快排
"""
快排在荷兰国旗问题上扩展，就是针对数组的每一个数据做patitaion划分，当所有的数据都划分完毕后，整个数组就排序完成了
在快排划分是有一些小的变化，就是在选定num时，通常按照数据中的最后一个数据作为num基准，然后在前面所有的数据中以num为基准进行patition，当分区完成后，把分区右侧>num区域的边界r的第一个位置r的数据和一开始就选中的数据num交换,示意如下
[<=num,>num,num]->[<=num,num,>num]
然后num的partition划分完成，返回最终num的下标，这意味着，num已经找到它在数组中的位置，然后在分别对num的下标index的
左侧0~index-1以及右侧index+1~len(arr)的数据进行递归的调用partition过程即可
"""
def sort_patition(li,l,r)->int:
    """入参为左右边界，返回值为确定的元素的下标"""
    if l>=r: #  当l和r相遇时，不再进行partition
        return None;
    num = li[r]
    r_cp = r
    index = l
    # l在一开始进入循环之前，就是在预设的<num的左边界的下一个位置了，所以在后续交换时，不用指定l+1
    while index < r:
        if li[index] < num:
            li[index],li[l] = li[l],li[index]  # 因为每次l+=1时，已经预跳转到了左边小于<num的下一个位置了，座椅这里不同使用l+1下标
            l += 1
            index += 1
        elif li[index] > num:
            li[index],li[r-1] = li[r-1],li[index]
            r -= 1
        else:
            index += 1

    li[r],li[r_cp] = li[r_cp],li[r] # 因为一开始选择的是最右侧的数据作为基准num,所以在while循环完后，确定了num的分界线，那么直接把基准值放在 右侧>num的区域的第一个位置，这里通过调换num和最后的r边界上的两者元素位置实现
    return r

def sort_patition2(li,l,r):
    """入参同sort_partition,但是返回的是一个边界元组
        这种是对第一个aort_patition的优化，当数组li中有相同的数据num的时候，在partition完成后，返回相同的num的数据的边界
        那么下次在快排再度调用该函数的时候，就不用针对形同的num的重复数据进行partition了
    """
    if l>=r:
        return
    num = li[r]
    r_cp = r
    index = l
    while index < r:
        if li[index] < num:
            li[index],li[l] = li[l],li[index]
            l += 1
            index += 1
        elif li[index] > num:
            li[index],li[r-1] = li[r-1],li[index]
            r -= 1
        else:
            index += 1
    li[r_cp],li[r] = li[r],li[r_cp]

    return (l,r)

def process_sort(li:list,l,r):
    """对li列表中，l->r区域范围的数据递归进行partition"""
    if l >= r:
        return
    m = sort_patition(li,0,r)

    process_sort(li,l,m-1)
    process_sort(li,m+1,r)

def process_sort2(li,l,r):
    """使用优化的paritition，对于有相同的num基准数据的数组，在某次partition分区后，不在进行重复数据的递归操作"""
    if l>=r:
        return
    m_area = sort_patition2(li,l,r)
    if len(m_area) > 1:
        process_sort2(li,l,m_area[0]-1)
        process_sort2(li,m_area[1]+1,r)
    else:
        process_sort2(li,l,m_area[0]-1)
        process_sort2(li,m_area[0]+1,r)

def quick_sort(li):
    # process_sort(li,0,len(li)-1)
    process_sort2(li,0,len(li)-1)

li=[random.randint(0,100) for _ in range(15)]
quick_sort(li)
print(li)

# 快排的最终版本
# 在快排选中某个基准之后，当这个基准值的左右数据的大小规模差不多的时候，快排的时间复杂度是最优的
# 故在每次选中基准值的时候，不再按照每次选数组最末尾的的数来作为基准值，而是随机的选取一个数据，结合荷兰国旗排序
# 在随机选中某个数据后，把数据和数组的最后一个数据进行交换，位置，然后带入partition，即可，
# ？其实就是多了一步，随机选值然后交换到数组末尾

def sort_patition3(li,l,r):
    if l >= r:
        return
    i = random.randint(0,r-l+1)
    li[i],li[r] = li[r],li[i]
    index = l
    r_cp = r
    num = li[r]
    while index <r:
        if li[index] < num:
            li[index],li[l] = li[l],li[index]
            l += 1
            index += 1
        elif li[index] > num:
            li[index],li[r-1] = li[r-1],li[index]
            r -= 1
        else:
            index += 1

    li[r],li[r_cp] = li[r_cp],li[r]
    return (l,r)

def process_sort3(li,l,r):
    if l>= r:
        return
    m_area = sort_patition3(li,l,r)
    if len(m_area) > 1:
        process_sort3(li,l,m_area[0]-1)
        process_sort3(li,m_area[1]+1,r)
    else:
        process_sort3(li,l,m_area[0]-1)
        process_sort3(li,m_area[0]+1,r)

def quick_sort3(li):
    # process_sort(li,0,len(li)-1)
    process_sort3(li,0,len(li)-1)

"""
patirion的应用:
把单向链表按照值划分为左边小，中间相等，右边大的形式

依然是荷兰国旗问题，
方法1：遍历链表，把值提取出来放在数组中，然后使用partition排序数组，排序后再把数组中的数据依次填充回链表中即可
方法2：直接在链表上进行partition划分
"""
from LinkList import Link,Node
l = Link()
# for each in (random.randint(0,100) for _ in range(10)):
for each in [64,2,3,79, 91 ,86,6 ,27, 39 ,71 ,85 ,6, 6]:
    l.add(each)
def partitionLink(link:Link,pre_lnode,rnode):
    num = rnode.var
    lnode = pre_lnode.next # 需要保留前置节点，在partition完成后，能够使用前直节点来指向排序区

    LH,LT,MH,MT,GH,GT = None,None,None,None,None,None
    node = lnode
    while node.next: # 在node还没有和rnode相遇之前，从lnode开始遍历
        print(f'check:{node.var} and num {num}')
        if node.var < num:
            if not LH:
                LH = node
                LT = LH
            else:
                LT.next = node
                LT = node
        elif node.var > num:
            if not GH:
                GH = node
                GT = node
            else:
                GT.next = node
                GT = node
        else:
            if not MH:
                MH = node
                MT = node
            else:
                MT.next = node
                MT = node
        node = node.next
    if not MH:
        MH = node
        MT = MH
    else:
        MT.next = node
        MT=node

    head = None
    if LT : # 如果有小于区域
        head = LH
        LT.next = MH
    else:
        head = MH

    MT.next = GH
    if GH: # 如果有大于区域
        GT.next = None

    pre_lnode.next = head

l.travel()
partitionLink(l,l[0],l[len(l)-1])
l.travel()


