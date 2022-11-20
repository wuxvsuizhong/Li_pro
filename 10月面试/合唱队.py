'''
N 位同学站成一排，音乐老师要请最少的同学出列，使得剩下的 K 位同学排成合唱队形。

设KK位同学从左到右依次编号为 1，2…，K ，他们的身高分别为T1,T2,…,TK，若存在i(1≤i≤K) 使得T1<T2<......<T{i-1}<Ti
​且 Ti>T{i+1}>......>TK，则称这KK名同学排成了合唱队形。
通俗来说，能找到一个同学，他的两边的同学身高都依次严格降低的队形就是合唱队形。
例子：
123 124 125 123 121 是一个合唱队形
123 123 124 122不是合唱队形，因为前两名同学身高相等，不符合要求
123 122 121 122不是合唱队形，因为找不到一个同学，他的两侧同学身高递减。

你的任务是，已知所有N位同学的身高，计算最少需要几位同学出列，可以使得剩下的同学排成合唱队形。

注意：不允许改变队列元素的先后顺序 且 不要求最高同学左右人数必须相等

数据范围：1≤n≤3000

输入描述：
用例两行数据，第一行是同学的总数 N ，第二行是 N 位同学的身高，以空格隔开

输出描述：
最少需要几位同学出列

示例1
输入：
8
186 186 150 200 160 130 197 200
输出：
4
说明：
由于不允许改变队列元素的先后顺序，所以最终剩下的队列应该为186 200 160 130或150 200 160 130
'''
def main():
    quantity = int(input().strip())
    team = list(map(int,input().strip().split()))

    dp_inc = [1 for _ in range(len(team))]
    for i,cur_height in enumerate(team):
        for j,height in enumerate(team[:i+1]):
            if cur_height > height:
                dp_inc[i] = max(dp_inc[j]+1,dp_inc[i])

    dp_dec = [1 for _ in range(len(team))]
    rteam = team[:]
    rteam.reverse()
    for i,cur_height in enumerate(rteam):
        for j,height in enumerate(rteam[:i+1]):
            if cur_height > height:
                dp_dec[i] = max(dp_dec[j]+1,dp_dec[i])

    dp_dec.reverse()


    # print(dp_dec,dp_inc)
    dp = [v1+v2-1 for v1,v2 in zip(dp_inc,dp_dec)]
    # print(dp)
    ret = dp.index(max(dp))
    print(len(team)-dp[ret])


if __name__ == '__main__':
    main()