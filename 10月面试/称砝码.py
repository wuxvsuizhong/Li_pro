'''
现有n种砝码，重量互不相等，分别为 m1,m2,m3…mn ；
每种砝码对应的数量为 x1,x2,x3...xn 。现在要用这些砝码去称物体的重量(放在同一侧)，问能称出多少种不同的重量。

注：

称重重量包括 0

数据范围：每组输入数据满足 1≤n≤10,1≤mi≤2000,1≤xi≤10
输入描述：
对于每组测试数据：
第一行：n --- 砝码的种数(范围[1,10])
第二行：m1 m2 m3 ... mn --- 每种砝码的重量(范围[1,2000])
第三行：x1 x2 x3 .... xn --- 每种砝码对应的数量(范围[1,10])
输出描述：
利用给定的砝码可以称出的不同的重量数

示例1
输入：
2
1 2
2 1
输出：
5
说明：
可以表示出0，1，2，3，4五种重量。
'''


def main():
    # 深度搜索，砝码量多的时候容易超时
    types = int(input().strip())
    vars = []
    for i in range(2):
        vars.append(list(map(int, input().strip().split())))

    # print(vars)
    weights = vars[0]
    quantitie = vars[1]
    w = []
    for i, v in enumerate(weights):
        for i in range(quantitie[i]):
            w.append(v)
    w.sort()
    print(w)


    rec = [False for _ in range(len(w))]
    # res = set([0])
    res = []

    def dfs(sumval, pos, step):
        # print(sumval)
        # res.add(sumval)
        res.append(sumval)
        if step >= len(w):
            return

        for i in range(pos, len(w)):
            if not rec[i]:
                if i > pos and w[i] == w[i - 1] and rec[i - 1] is False: continue
                rec[i] = True
                sumval += w[i]
                dfs(sumval, i + 1, step + 1)
                rec[i] = False
                sumval -= w[i]

    dfs(0, 0, 0)

    print(len(res))


if __name__ == '__main__':
    main()
