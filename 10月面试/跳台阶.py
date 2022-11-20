'''
一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个 n 级的台阶总共有多少种跳法（先后次序不同算不同的结果）

输入：
2
返回值：
2
说明：
青蛙要跳上两级台阶有两种跳法，分别是：先跳一级，再跳一级或者直接跳两级。因此答案为2
'''
import sys
def main():
    n = int(sys.stdin.readline().strip())
    dp = [0 for _ in range(n+1)]

    for i in range(n+1):
        if i == 0:
            dp[i] = 0
        if i <= 2:
            dp[i] = i
        else:
            dp[i] = dp[i-1] + dp[i-2]

    print(dp[-1])

def deep_search():
    n = int(input().strip())
    steps = [1,2]
    res = []
    book = [True for _ in range(len(steps))]
    def dfs(cur_hei,stps,book):
        if cur_hei > n:
            return
        elif cur_hei == n:
            res.append(stps+1)
            return

        nbook = book[:]
        for i,st in enumerate(steps):
            if book[i]:
                book[i] = False
                dfs(cur_hei+st,stps+1,nbook)
                book[i] = True
    dfs(0,0,book)

    print(len(res))


if __name__ == '__main__':
    # main()
    deep_search()