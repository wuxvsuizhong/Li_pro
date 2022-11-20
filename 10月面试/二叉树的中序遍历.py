class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def mid_add(list,root):
    if not root:
        return

    mid_add(list,root.left)
    list.append(root.val)
    mid_add(list,root.right)

def inorderTraversal(root):
    list=[]
    mid_add(list,root)
    for each in list:
        print(each)