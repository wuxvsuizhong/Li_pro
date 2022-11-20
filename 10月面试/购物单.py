'''
王强决定把年终奖用于购物，他把想买的物品分为两类：主件与附件，附件是从属于某个主件的，下表就是一些主件与附件的例子：
主件	附件
电脑	打印机，扫描仪
书柜	图书
书桌	台灯，文具
工作椅	无
如果要买归类为附件的物品，必须先买该附件所属的主件，且每件物品只能购买一次。
每个主件可以有 0 个、 1 个或 2 个附件。附件不再有从属于自己的附件。
王强查到了每件物品的价格（都是 10 元的整数倍），而他只有 N 元的预算。除此之外，他给每件物品规定了一个重要度，用整数 1 ~ 5 表示。他希望在花费不超过 N 元的前提下，使自己的满意度达到最大。
满意度是指所购买的每件物品的价格与重要度的乘积的总和，假设设第i件物品的价格为v[i]，重要度为w[i]，共选中了k件物品，编号依次为j1,j2,...,jk ，则满意度为：v[j1]*w[j1]+v[j2]*w[j2]+ … +v[jk]*w[jk]（其中 * 为乘号）
请你帮助王强计算可获得的最大的满意度。


输入描述：
输入的第 1 行，为两个正整数N，m，用一个空格隔开：
（其中 N （ N<32000 ）表示总钱数， m （m <60 ）为可购买的物品的个数。）
从第 2 行到第 m+1 行，第 j 行给出了编号为 j-1 的物品的基本数据，每行有 3 个非负整数 v p q
（其中 v 表示该物品的价格（ v<10000 ）， p 表示该物品的重要度（ 1 ~ 5 ）， q 表示该物品是主件还是附件。如果 q=0 ，表示该物品为主件，如果 q>0 ，表示该物品为附件， q 是所属主件的编号）

输出描述：
 输出一个正整数，为张强可以获得的最大的满意度。
示例1
输入：
1000 5
800 2 0
400 5 1
300 5 1
400 3 0
500 2 0
输出：
2200
示例2
输入：
50 5
20 3 5
20 3 5
10 3 0
10 2 0
10 1 0
输出：
130
说明：
由第1行可知总钱数N为50以及希望购买的物品个数m为5；
第2和第3行的q为5，说明它们都是编号为5的物品的附件；
第4~6行的q都为0，说明它们都是主件，它们的编号依次为3~5；
所以物品的价格与重要度乘积的总和的最大值为10*1+20*3+20*3=130
'''
def main():
    money,quantity = map(int,input().strip().split())
    prices,importances,attch_rec = [0],[0],[0]
    for _ in range(quantity):
        price,importance,isattach = map(int,input().strip().split())
        prices.append(price)
        importances.append(importance)
        attch_rec.append(isattach)
    #
    # print("prices",prices)
    # print("importances",importances)

    attchs = {}
    for i in range(1,len(attch_rec)):
        if attch_rec[i] != 0:
            if attch_rec[i] in attchs:
                attchs[attch_rec[i]].append(i)
            else:
                attchs[attch_rec[i]] = [i]

    # print("attachs",attchs)

    def get_combination(grp,nums,pos,rec,res):
        if grp:
            res.append(grp[:])
        if len(grp) == len(nums):
            return
        for i in range(pos,len(nums)):
            if not rec[i]:
                rec[i] = True
                grp.append(nums[i])
                get_combination(grp,nums,pos+1,rec,res)
                rec[i] = False
                grp.pop()

    for k,vals in attchs.items():
        res=[]
        rec = [False for _ in range(len(vals))]
        get_combination([],vals,0,rec,res)
        for i in range(len(res)):
            res[i].append(k)
        res.append([k,])
        attchs[k] = res[:]

    # print(attchs)
    for i in range(1,len(prices)):
        if attch_rec[i] == 0 and i not in attchs:
            attchs[i] = []
            attchs[i].append([i,])


    attchs_grp_prices,attchs_grp_weight = [[0,],],[[0,],]
    for k,vals in attchs.items():
        tmp_grp_prices=[]
        tmp_grp_wei=[]
        for itm in vals:
            tmp_grp_prices.append(sum([prices[i] for i in itm]))
            tmp_grp_wei.append(sum([v1*v2 for v1,v2 in zip([prices[i] for i in itm],[importances[i] for i in itm])]))
        attchs_grp_prices.append(tmp_grp_prices)
        attchs_grp_weight.append(tmp_grp_wei)

    print("attchs", attchs)
    print("attchs_grp_prices",attchs_grp_prices)
    print("attchs_grp_weight",attchs_grp_weight)

    dp = [[0 for _ in range(money+1)] for _ in range(len(attchs_grp_prices))]

    for i in range(1,len(attchs_grp_prices)):
        for j in range(1,money+1):
            for k,v in enumerate(attchs_grp_prices[i]):
                # print(v)
                if v > j:
                    dp[i][j] = max(dp[i-1][j],dp[i][j])
                else:
                    dp[i][j] = max(dp[i-1][j],dp[i-1][j-v]+attchs_grp_weight[i][k],dp[i][j])
                    # print(dp[i][j])




    # print(dp)/
    print(dp[-1][money])
#
# def main1():
#     while True:
#         try:
#             total_money, total_num = map(int, input().split(' '))
#             total_money //= 10
#             product_item = []
#             for i in range(total_num):
#                 v, p, q = map(int, input().split(' '))
#                 v //= 10
#                 product_item += [[i + 1, v, p, q]]
#             dp = [[0, [0]] for i in range(total_money + 1)]
#
#             for current_no, v, p, q in product_item:
#                 for i in range(len(dp) - 1, -1, -1):
#                     if (i - v) >= 0:
#                         if not current_no in dp[i - v][1]:
#                             if q in dp[i - v][1]:  # the parent has been chosen.
#                                 if (dp[i - v][0] + v * p) > dp[i][0]:
#                                     dp[i][0] = dp[i - v][0] + v * p
#                                     dp[i][1] = dp[i - v][1].copy()
#                                     dp[i][1] += [current_no]
#                             else:  # the parent has not been chosen, then we can pick up both current one and the parent.
#                                 if (i - v - product_item[q - 1][1]) > 0:
#                                     if (dp[i - v - product_item[q - 1][1]][0] + v * p + product_item[q - 1][1] *
#                                         product_item[q - 1][2]) > dp[i][0] and not current_no in \
#                                                                                    dp[i - v - product_item[q - 1][1]][
#                                                                                        1] and not q in dp[
#                                         i - v - product_item[q - 1][1]][1]:
#                                         dp[i][0] = dp[i - v - product_item[q - 1][1]][0] + v * p + product_item[q - 1][
#                                             1] * product_item[q - 1][2]
#                                         dp[i][1] = dp[i - v - product_item[q - 1][1]][1].copy()
#                                         dp[i][1] += [current_no]
#                                         dp[i][1] += [q]
#             print(dp[total_money][0] * 10)
#         except:
#             break

if __name__ == '__main__':
    main()