'''
给定两个整数 n 和 k，返回范围 [1, n] 中所有可能的 k 个数的组合。
你可以按 任何顺序 返回答案。

示例 1：
输入：n = 4, k = 2
输出：
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]

示例 2：
输入：n = 1, k = 1
输出：[[1]]

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/combinations
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
'''

import copy
def main():
    vrange,quantity = list(map(int,input().strip().split()))
    allnum = [i+1 for i in range(vrange)]
    opmap =[False for _ in range(vrange)]
    res = []

    def dfs(nums,result,pos):
        if len(nums) == quantity:
            res.append(copy.copy(nums))
            return

        # for i,n in enumerate(allnum):
        for i in range(pos,len(allnum)):
            if not opmap[i]:
                opmap[i] = True
                nums.append(allnum[i])
                dfs(nums,result,i+1)
                opmap[i] = False
                nums.pop()

    dfs([],res,0)
    print(res)


if __name__ == '__main__':
    main()