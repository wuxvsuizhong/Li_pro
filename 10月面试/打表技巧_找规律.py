'''
小胡去买苹果，商店只提供两种类型的塑料袋，每种类型的塑料岛数量不限
1.能装下6个苹果的塑料袋子
2.能装下8个苹果的塑料袋子

小胡可以自由使用两种袋子来装苹果，但是小胡渔鸥强迫症，他是要求自己使用的袋子必须最少，且每个单子必须装满
给定一个正整数N,返回至少使用多少袋子，如果不存在，返回-1
'''
import math

def process(n:int)->int:
    val,rest = divmod(n,8)
    if rest:  # 当优先选用装8个苹果的袋子装不完时
        while val >= 0:
            val2,rest2 = divmod(n-val*8,6)    # 每减少使用8的袋子，尝试用装6的袋子去装苹果
            if rest2 == 0:
                return val+val2
            val -= 1
        return -1
    else:
        return val


def process2(n: int) -> int:
    """总结暴力递归的结果规律"""
    if n < 11:
        if n == 6 or n == 8:
            return 1
        else:
            return -1

    if n >= 11 and n % 2:
        return -1
    if 11 < n < 18 and n % 2 == 0:
        return 2
    if n >= 18 and n % 2 == 0:
        return int((n - 18) / 8) + 3

# if __name__ == "__main__":
#     for i in range(1,101):
#         # print(i,":",process(i))
#         # print(i,process(i),process2(i))
#         if process(i) != process2(i):
#             print(f"{i} not good")

'''
给定一个正整数N表示有N分青草，有一只羊和一头牛，牛先吃，羊后吃，他两轮流吃草，不论是牛还是羊，每次吃草的数量都是4的某次方，比如1,4，16,64等。
谁先把草吃完，谁获胜。假设牛和羊都是聪明的，都想最终能赢，每次都能做出合理的的决定，给定唯一的参数N,返回谁会赢

解析：谁最后能赢，是采取适当的措施能够使得后手面临无草可吃的情况时，那么此时先吃光草的就能先赢。
当N=0时，先吃草的先面临无草可吃的情况，此时先吃草的输，后吃草的赢了；
N=1时，先吃草的吃掉，那么后吃草的面临无草可吃，所以先吃草的赢
N=2时，因为每次吃草数量的限制，且每一轮必须吃草，所以先吃草的必须吃1份，后吃草的再吃一份，然后原本最开始先吃草的面临无草可吃，所以此时后吃草的赢了。。。
N=3时，同理可得先吃草的赢。
N=4时，因为吃草的都能做出明智的选择，所以，此时先吃草的吃掉4分，让后吃草的无草可吃，先手赢
N=5时，先吃草的第一次吃掉4分，然后后吃草的只能吃掉一份，那么后吃草的赢。如果先吃草的迟到4分，后吃草的吃掉1分，那么还是后吃草的赢，，所有N=5时，先吃草的一定赢

其实在N>4以后，每次吃草的动物面对的场景无非是1~4的循环，只是谁先谁后的角色转换而已
'''
# 一开始是牛先吃
def eat_glass_winner(N:int,first:str)->str:
    if 0<=N<5:
        if N in (0,2): # 后吃草的胜
            winner = '羊' if first == '牛' else '牛'
        else: # 先吃草的胜
            winner = '牛' if first == '牛' else '羊'

        return winner

    ret = math.log(N)/math.log(4)
    if ret == int(ret):
        winner = '牛' if first == '牛' else '羊'
        return winner

    base = 1
    second = '羊' if first == '牛' else '牛'
    while base <= N:
        if eat_glass_winner(N-base,second) == first:
            return first
        base *= 4
    return second

def eat_glass_winner2(N:int):
    '后先后先先'
    rec = {
        0:"羊",
        1:"牛",
        2:"羊",
        3:"牛",
        4:"牛",
    }

    return rec[N%5]

# if __name__ == "__main__":
#     for i in range(50):
#         # print(i,eat_glass_winner(i,'牛'))
#         if eat_glass_winner(i,"牛") != eat_glass_winner2(i):
#             print("not good")


'''
定义一种数，可以表示成若干的(数量>1)的连续正数的和的数，比如：
5=2+3
12=3+4+5
1不是这样的数，因为需要数量大于1，连续正数和2也不是，2=1+1,因为是两个相等的数相加，不满足是连续的正数

给定一个数N,返回是不是可以表示成若干的连续正数的和的数

解析：有限范围暴力求解+找规律
'''

def judge_seq_add_number(N:int)->bool:
    """判断一个数是否可以由连续相加的数组成"""
    index = 1
    while index < N:
        s = 0
        for i in range(index,N):
            s += i
            if s == N: return True
            if s > N: break
        index += 1
    return False
# 通过打印结果可以看出，只要数据是2的某次方的结果，那么，数据就可以是连续的数的加和
def judge_seq_add_number2(N:int)->bool:
    """判断数据是不是2的某个次方
    如果数据是2的某次方(0,1,2,4,8,16...)，那么在2进制的形式上，只有一个1，这时候，在N-1的情况下，将把唯一的1后面的位数都变成1，而原来的1位置的变为0，那么就有N&(N-1) == 0成立
    """
    if N <= 2 or N&(N-1) == 0:   # 当N<=2或者N是否是2的某次方
        return False
    return True



if __name__ == "__main__":
    for i in range(1000):
        # if not judge_seq_add_number(i):
        #     print(i,"False")
        if judge_seq_add_number(i) != judge_seq_add_number2(i):
            print('not good',i,judge_seq_add_number(i),judge_seq_add_number2(i))










