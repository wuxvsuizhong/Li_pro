'''
有重复字符串的排列组合。编写一种方法，计算某字符串的所有排列组合。
示例1:

 输入：S = "qqe"
 输出：["eqq","qeq","qqe"]

示例2:
 输入：S = "ab"
 输出：["ab", "ba"]
提示:

字符都是英文字母。
字符串长度在[1, 9]之间。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/permutation-ii-lcci
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
'''


def main():
    l = input().strip()
    ops = [False for _ in range(len(l))]
    res = []
    dfs(ops, '', l, res)
    print(res)


def dfs(opmap, s, origstr, res):
    if False not in opmap:
        res.append(s)
        return
    for i, v in enumerate(opmap):
        if not v:
            opmap[i] = True
            dfs(opmap, s + origstr[i], origstr, res)
            opmap[i] = False


class Solution:
    def permutation(self, S):
        # l = input().strip()
        self.ops = [False for _ in range(len(S))]
        self.res = []
        self.S = S
        self.dfs('')
        self.res = self.sortresult()
        # print(self.res)
        return self.res

    def dfs(self, s):
        if len(s) == len(self.S):
            self.res.append(s)
            return

        for i, v in enumerate(self.ops):
            if not v:
                if i> 0 and  self.S[i] == self.S[i - 1] and self.ops[i-1] is False:
                    continue
                #剪枝，对于某一层递归，其可选的除了上层已经选择的元素除外，在本层选择的时候
                #第二次选的不能和本层递归之前一次选择的元素相同,例如pppppHHHHH
                #在第一层可选的只有两个元素p或者H
                #在第二层可选的除了第一层选过的p和H之外，第二层选择只有两个，一个p另外一个H
                #所以对于某个重复的元素，在某轮选择时只能选择一次，不能选择第二次，以达到剪枝的目的
                self.ops[i] = True
                self.dfs(s + self.S[i])
                self.ops[i] = False

    def sortresult(self):
        sortres = []
        for i, each in enumerate(self.res):
            if self.res.index(each) == i:
                sortres.append(each)
        sortres.sort()

        return sortres

class Solution1:
    def permutation(self, S):
        n=len(S)
        if n==0:
            return [""]
        res=[]
        for i in range(n):
            if S[i] in S[:i]:   #只需判断S[i]是否在S[:i]中出现过即可
                continue
            for s1 in self.permutation(S[:i]+S[i+1:]):
                res.append(S[i]+s1)
        return res
        # print(res)


if __name__ == '__main__':
    # main()
    s = Solution()
    print(s.permutation('pppppHHHH'))
    # print(s.permutation('abc'))
