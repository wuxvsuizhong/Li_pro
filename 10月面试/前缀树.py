# 前缀树的定义
"""
单个字符串上，字符从前到后的加到一棵多叉树上
字符放在路上，节点上优专属的数据项(常见的是pass和end值）
所有的字符串样本都这样添加，如果没有路就新建，如果有路就复用
添加字符串字符时，沿途只要在添加的时候经过节点，那么pass值就加1，每个字符串结束时来到的节点end值就加1

前缀树又称为字典树，常用来完成前缀相关的查询操作
"""
import typing

class Node:
    def __init__(self,c):
        self.ch = c
        self.passno = 0
        self.end = 0
        self.nexts = {}

    def __repr__(self):
        return f'ch:{self.ch} passno:{self.passno} end:{self.end} nexts:{self.nexts.keys()}'

class TrieTree:
    def __init__(self):
        self._root = Node('#')
    def insert(self,s:str):
        if not s:
            return
        node = self._root
        node.passno += 1
        for c in s:
            if c not in node.nexts:
                node.nexts[c] = Node(c)
            node = node.nexts[c]
            node.passno += 1

        node.end += 1


    def travel(self):
        node = self._root

        def show(node):
            for each in node.nexts:
                print(f'{node.nexts[each]!r}')
                show(node.nexts[each])
            return
        return show(node)

    def search(self,s):
        """查找字符串s被加入几次"""
        node = self._root
        for c in s:
            if c not in node.nexts:
                return None
            node = node.nexts[c]
        return node.end

    def delete(self,s):
        """从前缀树中删除s"""
        res = self.search(s)
        if res and res > 0:
            node = self._root
            node.passno -= 1
            # for c in s:
            #     node.passno -= 1
            #     if node.passno == 0:
            #         node.nexts.clear()
            #         return
            #     node = node.nexts[c]
            for c in s:
                if node.nexts[c].passno == 1:
                    del node.nexts[c]   # 删除前需要保持node的坐标依然位于父级node上，删除时在父级的node上，按照del dict[key]方式删除
                    return
                node = node.nexts[c]
            node.end -= 1




tree = TrieTree()
tree.insert('abcddf')
tree.insert('abce')
tree.insert('alksdnfqwli')
tree.insert('cdef')
tree.insert('abce')

tree.travel()

print(tree.search('abce'))
tree.delete('abce')
print('delete "abce"')
tree.travel()
print('delete "alksdnfqwli"')
tree.delete('alksdnfqwli')
tree.travel()




