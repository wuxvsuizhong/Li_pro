import collections
import copy
import dataclasses
import random
import typing

import binarytree

valus = [random.randint(0,100) for _ in range(15)]
# valus = [99, 87, 39, 85, 2, 34, 78, 75, 42, 92, 31, 8, 100, 54, 89]
print("valus:",valus)
tree = binarytree.build(valus)
print(tree)

def head_first(head:binarytree.Node):
    """先序遍历"""
    if not head: return
    print(head.value,end=' ')
    head_first(head.left)
    head_first(head.right)

head_first(tree);print("<-先序遍历")

def head_mid(head:binarytree.Node):
    """中序遍历"""
    if not head:return
    head_mid(head.left)
    print(head.value,end= ' ')
    head_mid(head.right)
head_mid(tree);print("<-中序遍历")

def head_last(head:binarytree.Node):
    """后序遍历"""
    if not head: return
    head_last(head.left)
    head_last(head.right)
    print(head.value,end= ' ')
head_last(tree);print("<-后序遍历")

def head_first_norecursion(head:binarytree.Node):
    """非递归版本的先序遍历，通过栈结构实现"""
    stack = collections.deque()
    stack.append(head)
    while stack:
        node = stack.pop()
        print(node.value,end= ' ')
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    print("<-非递归版本先序遍历")

head_first_norecursion(tree)

def head_mid_norecursion(head:binarytree.Node):
    """非递归版本中序遍历"""
    stack = collections.deque()   # 注意无需在循环之外压入任何节点
    while stack or head:
        if head:
            stack.append(head)
            head = head.left
        else:
            head = stack.pop()
            print(head.value,end=' ')
            head = head.right
    print("<-非递归版本中序遍历")
head_mid_norecursion(tree)

def head_last_norecursion(head:binarytree.Node):
    """非递归版本后序遍历
    后序遍历相对于前面的两种，实现思路上有所区别,可以从节点的压栈，出栈来考虑。
    后序遍历先要找到树的左子树的最左节点，那么向下的时候必然先第一次经过子树的头结点，然后找到子树的最底部的左节点，打印
    然后返回其头结点，此时是返回子树的头结点，也就是第二次经过子树头结点的，但是此时还不能打印字数的头结点，而是需要遍历子树的右节点，如果当访问到达底部的子树右节点，那么打印右节点，然后返回到头结点，这时候返回就是对子树头结点的第三次访问。此时才能打印头结点。

    也就是说，在后序遍历时，对于底部的节点，只访问一次然后打印返回即可，但是对于子树的头结点，如果头结点的左右子树(或者节点)存在的时候，头结点需要在返回的第三次访问的时候再打印。

    那么判断一个节点是否压栈，分一下情况：
    压栈：任意的节点，在第一次访问时压栈，不论是子树头结点还是底部的叶子结点
    出栈：当节点无左右子节点时，也就是叶子节点直接打印然后出栈，出栈时pre指针记录节点。
         当节点有左右子节点时，如果pre指针和当前节点的左子树相等，也就是之前出栈的是左边的子节点，那么当前节点就是子树的头部节点，此时保留头结点不处理，转而去压入当前节点的右子节点。
         当节点有左右子节点时，如果per指针和当前节点的右节点相等，那么，说明上次出栈打印的是节点的右子节点，此时当前节点出栈并打印，并记录为pre。

    这也从侧面说明，只要子树中有pre指针的记录，那么说明当前子树已经有节点参与出栈并打印了;
    并且，pre的记录总是先左节点，再右节点，如果只是左节点标记了pre，那么说明此时该处理右节点，而如果是右节点被标记pre，说明左右节点都已被处理，直接处理子树头结点，然后向上原路返回访问，
    """

    stack = collections.deque()
    stack.append(head)
    # while stack:
    #     c = stack[-1] # c指向栈中的栈顶
    #     if c.left and head != c.left and head != c.right: # 当前遍历的节点head不是当前栈顶指向的节点的左或者右节点
    #         stack.append(c.left) # 当前遍历的节点的左节点压栈
    #     elif c.right and head!=c.right: # 当前遍历的节点head不是当前栈顶指向的节点的右节点
    #         stack.append(c.right) # 当前遍历的节点的右节点压栈
    #     else:
    #         node = stack.pop() # 栈顶出栈
    #         print(node.value,end= ' ')
    #         head = c # 当前遍历的节点指向栈顶节点
    pre = None
    while stack:
        head = stack[-1]
        if head.left or head.right:  # 左右子树是要有一边存在的时候，先判断子树中是否有节点弹出打印过，即是否有pre标记
            if pre == head.left and head.right:  # 左子树标记过pre，且有右侧子节点，那么直接压入右侧节点
                stack.append(head.right)
            elif pre == head.right: # 右子树标记过pre,那么直接弹出当前节点，并标记pre
                pre = stack.pop()
                print(pre.value,end=' ')
            else:  # 没有pre标记，说名当前节点下的子树都没有被访问过，当左节点存在时优先压入左节点，如果不存在那么压入右节点
                if head.left:
                    stack.append(head.left)  # pre没有在左右节点标记过，那么是第一次访问该节点，如果左节点存在直接压栈
                else: # pre没有标记过子节点，那么是第一次访问该节点，但是节点只有右侧子节点，那么压栈右测节点
                    stack.append(head.right)
        else: # 当左右子树都不存在的时候，也就是达到了底部节点，直接出栈，并标记节点pre
            pre = stack.pop()
            print(pre.value, end=' ')
    print('<-非递归版本后序遍历')

head_last_norecursion(tree)

def floor_travel_tree(head:binarytree.Node):
    """层级遍历二叉树,借助队列实现"""
    q = collections.deque()
    q.append(head)
    while q:
        head = q.popleft()
        print(head.value,end=' ')
        if head.left:
            q.append(head.left)
        if head.right:
            q.append(head.right)
    print('<-二叉树层级遍历')

floor_travel_tree(tree)

"""
统计二叉树的那一层的宽度最大，也就是那一层的节点最多

需要有一种机制能够发现某一层的开始或者结束，这里留意，层级遍历的时候，节点的便利顺序总是在一层结束完了之后再开始下一层的。
所以可以利用层级遍历的这一特点。记录一个hash字典，记录层级节点和层级的关系
"""
def count_tree_maxwidth(head:binarytree.Node):
    """统计二叉树中哪一层的节点最多（结束hash字典)"""
    q = collections.deque()
    q.append(head)
    max_width,curlevel_nodes = 0,0
    level_map = {}  # 记录node-层级 的关系hash字典
    level_map[head] = 0
    rec_level = 0
    while q:
        node = q.popleft()
        if level_map[node] != rec_level:  # 从字典中查到的节点的层级和已有的记录不一样，说明当前已经访问到新的层级的节点了
            curlevel_nodes = 1
            rec_level = level_map[node] # 更新层级记录
        else:
            curlevel_nodes += 1
        max_width = curlevel_nodes if curlevel_nodes > max_width else max_width

        if node.left:
            level_map[node.left] = level_map[node] + 1
            q.append(node.left)
        if node.right:
            level_map[node.right] = level_map[node] + 1
            q.append(node.right)

    print(max_width)

print("二叉树的最大宽度:",end=' ');count_tree_maxwidth(tree)

def count_tree_maxwidth2(head:binarytree.Node):
    """不使用hash字典
    从头结点开始，头结点肯定是最开始层级的最末节点，然后一层层递推下去，提前获得层级的最末节点
    """
    last_node = head
    q = collections.deque()
    q.append(head)
    curlevel_nodes = 0
    max_width = 0

    while q:
        node = q.popleft()
        if node == last_node:
            max_width = curlevel_nodes+1 if curlevel_nodes +1 > max_width else max_width
            last_node = node.right if node.right else node.left # 提前找到下一层的最末节点
            curlevel_nodes = 0
        else:
            curlevel_nodes += 1

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    print("二叉树的最大宽度:",max_width)

count_tree_maxwidth2(tree)

"""
二叉树的序列化
比如对于如下的二叉树，进行序列化时，可以按照先序遍历的方式序列化，在节点为空的位置补None
      33                33     
     /                 /  \    
    81       ->       81   None    
      \              /   \      
       27           None  27    
                         /  \
	                    None None
那么先序遍历的打印结果就是:[33,81,None,27,None,None,None]
"""
# value = [33,81,None,None,27,None,None]
# tree2 = binarytree.build(value)
# print(tree2)

def head_first_marshal(head:binarytree.Node):
    """先序遍历序列化"""
    save = []
    def head_first(head):
        if not head:
            save.append("None")
            return
        else:
            save.append(head.value)

        head_first(head.left)
        head_first(head.right)

    head_first(tree)
    return save
value = head_first_marshal(tree)
print(value)

def head_first_unmarshal(values:collections.deque)->binarytree.Node:
    """先序方式逆序列化"""
    val = values.popleft()
    if val == "None":
        return
    node = binarytree.Node(val)
    node.left = head_first_unmarshal(values)
    node.right = head_first_unmarshal(values)

    return node

t = head_first_unmarshal(collections.deque(value))
print(t)

"""
中序后序的序列化，使用递归，然后调整程序递归调用的递归顺序即可
按照层级遍历的方式序列化，不用使用递归，但是也是需要把树节点为空的的地方补齐None即可
"""

"""
二叉树的结构如下:
Class Node:
    value
    left
    right
    parent
left,right分别为节点的左右子节点，parent节点是指向父级节点的指针，value是节点的值
给出二叉树的某个节点，按照中序遍历返回该节点的后继节点

解析:
如果节点是叶子结点：
    并且是父节点的左叶子结点，那么其后继节点是父节点；
    如果是父级节点的右节点，那么需要持续向上查找，直到找到某一集节点node，是其父级节点的左节点，那么该节点node的父级节点就是后继；
如果是非叶子节点：
    如果节点有右子树：
        那么后继节点就是右子树的最左侧叶子结点；
    如果节点无右子树：
        那么后继节点的逻辑可参照叶子节点，右节点的情况处理



如下二叉树的中序遍历顺序['i', 'e', 'j', 'b', 'k', 'f', 'a', 'g', 'd', 'h']
如果节点是父节点的左侧子节点，那么当前节点的后继节点就是父节点,如下面的b的后继是父节点a, e的后继是父节点b。
如果当前节点是父级节点的右侧子节点，那么持续向上查找，直到向上找到某个节点如果是其上层父节点的左侧子节点，那么该节点就是后继节点，如e的后继是a,c的后继

        ____a__
       /       \
    __b__       d
   /     \     / \
  e       f   g   h
 / \     /
i   j   k
"""

def get_head_mid_behind_node(head:binarytree.Node):
    """获取中序遍历的节点的后继节点"""
    def get_left_leaf(node):
        """获取以node为根节点的子树的最左侧叶子结点"""
        if not node: return None
        while node.left:
            node = node.left
        return node

    if not head: return None
    node = head

    if not (node.left and node.right): # 叶子节点
        if node == node.parent.left:   # 叶子节点是左侧节点
            return node.parent    # 返回节点的父节点就是后继
        else:
            while node != node.parent.left: # 向上遍历节点，直到找到一个左节点
                node = node.parent
            return node.parent #返回找到的左节点的父节点

    if node.right:  # 有右侧子节点
        return get_left_leaf(node)  # 获取右子树的最左侧节点
    else:
        while node != node.parent.left: # 向上遍历节点，直到找到一个左节点
            node = node.parent
        return node.parent #返回找到的左节点的父节点

'''
一张纸条，从中间对折一次后，打开把纸条凹面始终对着自己。然后恢复对折。
再持续的对折，期间始终保持最初面向自己的一面不变，多对这几次后，展开，会发现纸面上出现了凹凸交替的折痕
给定一个对折次数n,给出纸条对折n次后，纸面的凹凸顺序
例如，n=1时，答应"凹",n=2时，打印”凹“，”凹“，“凸”

解析：规律是凹面的左右两侧折痕的方向始终相反的，而做左侧的折痕始终是凹面

'''

def get_folds(i:int,n:int,direction:str):
    """打印纸条折痕,i:当前的层数，n总共对折多少次，direction:当前次的折痕的方向"""
    if i>n:
        return
    get_folds(i+1,n,'凹')
    print(direction,end=' ')
    get_folds(i+1,n,"凸")

get_folds(1,4,"凹")

'''
检查二叉树是否是平衡树

二叉平衡树的定义式，左右子树的高度差不超过1
'''
class Info(typing.NamedTuple):
    height:int
    isbalance:bool

def check_balance_tree(head:binarytree.Node)->Info:
    """判断以head开头的节点的二叉树是否是平衡树"""
    if head is None: return Info(0,True)  # 基本条件，当节点为空时，是平衡树，并返回高度为0
    leftinfo = check_balance_tree(head.left)  # 获取左子树的信息
    rightiinfo = check_balance_tree(head.right) # 获取右子树的信息

    height = max(leftinfo.height,rightiinfo.height)+1 # 去左右子树的做大高度，然后加1就是当前子树的高度
    isbalance = True
    if (not leftinfo.isbalance) or (not rightiinfo.isbalance) or abs(leftinfo.height-rightiinfo.height) > 1:
        # 左右子树只要有一方不是平衡树或者是左右子树的高度差大于1，那么就不是平衡树
        isbalance = False

    return Info(height,isbalance)

print("\n是否平衡树",check_balance_tree(tree).isbalance)

"""
二叉树的递归模板：
1）假设一head节点为头，假设可以向head.left和head.right要任何的信息
2）在上一步的假设下，谈论以head为头结点的数(与head有关和无关的情况)，得到答案的可能性(重要) 
3) 列出所有的可能性后，确定到底需要向左树和右树需要什么样的信息
4）把左树和右树的信息求全集，就是任何一棵树都需要返回的信息S
5) 递归函数都返回S,每一棵树都这样要求
6）写代码，在代码中考虑如何把左树的信息和右树的信息整合出整个树的信息
"""

"""
给定一个二叉树的头结点head,任意两个节点之间都存在距离，返回整个二叉树的最大距离

分析:
最大距离就是一个节点走向另外一个节点经过的节点个数，以head为例，如果两个节点之间的路径不经过head，那么两个节点只存在于head的子树中，如果两个节点的路径需要经过head，那么说明两个节点分别位于head的左右子树中；

而需要求最大距离，也分为经过head或者不经过head
如果是经过head,那么head树中的最大距离就是左子树的高度加上右子树的高度加上head的高度+1
如果是不经过head,那么head树中的最大距离就是，取左子树和右子树中的节点最大距离
"""

class Info(typing.NamedTuple):
    maxdistance:int
    height:int
def get_longest_distance(head:binarytree.Node)->Info:
    if head is None: return Info(0,0)

    leftinfo = get_longest_distance(head.left)
    rightinfo = get_longest_distance(head.right) # 向左右子树获取信息

    height = max(leftinfo.height,rightinfo.height)+1  # 当前子树的高度
    # 整合组左右子树的信息，获取最大值
    maxdistance = max(leftinfo.maxdistance,rightinfo.maxdistance,leftinfo.height+rightinfo.height+1)
    return Info(maxdistance,height)
print(tree)
print("树的最长距离:",get_longest_distance(tree).maxdistance)

'''
给定一个二叉树的头结点head,返回这个二叉树中最大的二叉搜索子树的最大头结点（提示：二叉搜索树是指，对所有的每一个节点而言，其左侧子树的节点的值都比节点的值小，而每一个节点的右子树的任意节点值，都比节点大，二叉搜索树没有重复节点)

分析：
取任意一个节点node,仍然是两种情况，最大的二叉搜索树和node无关，以及最大的二叉搜索树和node有关
和node无关，是指最大的二叉搜索树的头部节点不是node，而是在node的子树中,node和其子树无法构成二叉搜索树;
和node有关，则最大的二叉搜索树的头部节点就是node,且满足node左侧子树是搜索二叉树，且node的右侧子树也是搜索二叉树.左子树的最大值小于node，且右数的最小值大于node(BST的定义，右侧子树的任意节点值都大于头结点，那么只需判断最小节点和头结点的大小即可，如果虽小节点都满足大于node的值，那么右树的左右节点都满足)
'''

@dataclasses.dataclass
class Info:
    maxval:int
    minval:int
    headval:int
    isBST:bool
    maxSubBSTSize:int
def get_maxbst_size(head:binarytree.Node)->Info:
    """获取最大的二叉搜索子树的头结点"""
    if head is None:return None

    leftInfo = get_maxbst_size(head.left)
    rightInfo = get_maxbst_size(head.right)


    minval = head.value
    maxval = head.value
    if leftInfo:
        maxval = leftInfo.maxval if leftInfo.maxval > head.value else head.value
        minval = leftInfo.minval if leftInfo.minval < head.value else head.value

    if rightInfo:
        maxval = rightInfo.maxval if rightInfo.maxval > maxval else maxval
        minval = rightInfo.minval if rightInfo.minval < minval else minval

    maxSubBSTSize = 0
    headval = None
    # 和当前节点head无关的情况
    if leftInfo:
        maxSubBSTSize = leftInfo.maxSubBSTSize
        if leftInfo.headval:
            headval = leftInfo.headval

    if rightInfo:
        maxSubBSTSize = max(maxSubBSTSize,rightInfo.maxSubBSTSize)  # 注意选出的maxSubBSTSuize已经混淆了leftInfo和rightInfo，所以设置headval的时候需要再次从leftInfo和rightInfo的值在比较
        if rightInfo.headval:
            if rightInfo.maxSubBSTSize > leftInfo.maxSubBSTSize: # BST尺寸较大者优先设置为headval
                headval = rightInfo.headval
                # print(f'尺寸优先,{headval},{rightInfo.headval}')
            if rightInfo.maxSubBSTSize == leftInfo.maxSubBSTSize: # BST尺寸相同者，选取headval较大的设置为headval
                # print(f'尺寸相同,{headval},{rightInfo.headval}')
                headval = rightInfo.headval if rightInfo.headval > headval else headval

    isBST = False
    # 和当前节点head有关
    # head的左右子树是BST的情况
    # 左右子树有任一方为空的情况：如果左树为空且右树为BST，那么当右树BST的最小值都大于头结点的值时，头结点为新的BST头，右子树为空时同理
    # 如果左右子树都为空，那么当前节点也构成BST
    # 如果左右子树都不为空，那么需要左右子树都是BST，并且左树的最大值小于当前头结点值，右树的最小值大于当前头结点的值
    # 最大二叉搜索树的头结点：如果以上条件成立，那么当前节点和其子树组成新的BST，那么最大头结点就是当前节点
    if ((leftInfo is None) or (leftInfo.isBST)) and ((rightInfo is None) or (rightInfo.isBST)) \
            and ((leftInfo is None) or (leftInfo.maxval < head.value)) and ((rightInfo is None) or (rightInfo.minval > head.value)):
        isBST = True
        maxSubBSTSize = (0 if leftInfo is None else leftInfo.maxSubBSTSize) + (0 if rightInfo is None else rightInfo.maxSubBSTSize) + 1
        headval = head.value

    return Info(maxval,minval,headval,isBST,maxSubBSTSize)


print("最大BST子树的尺寸",get_maxbst_size(tree).maxSubBSTSize)
print("最大BST子树的头结点",get_maxbst_size(tree).headval)


'''
派对快乐的最大值

公司的每个员工都符合Employee的类描述，整个公司的员工可以看做是一颗标准的无环的多叉树。树的头结点是公司唯一的老板，除了老板之外每个员工都有直接的唯一上级。叶子结点是没有任何下属的基层员工(subordinates列表为空),除了基层员工之外，每个员工都有一个或者多个的直接下级。

现在公司举办party,你可以决定公司有那些员工来或者不来，规则:
1.如果员工来了，那么这个员工的所有直接下级，就不能来；
2.派对的整体快乐值是所有到厂员工的快乐值的累加；
3.目标是让快乐值最大。

给定一个多叉树的头结点boss，返回派对的最大快乐值

分析：
当轮到某个节点node时，依旧是分为node来或者是不来两种情况。
如果node不来，就是node本身的快乐值加上其所有下属的不来的快乐值的总和；
如果node来了，那么快乐值就是node本身的快乐值，加上其所有的下属的来或者不来的快乐值的总和，在来和不来之间求最大值
'''



