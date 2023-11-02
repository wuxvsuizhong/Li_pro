# #############
# 用于筛选的生成器
# #############
import itertools
def vowel(c):
    return c.lower() in 'aeiou'

if __name__ == "__main__":
    print('-'*20,"用于筛选的生成器",'-'*20)

    print(list(filter(vowel,'Aardvark')))   #['A', 'a', 'a'] 在可迭代对象中筛选满足条件的值比呢返回列表
    # itertools.fiterfalse 在迭代对象中筛选不满足条件的值返回列表
    print(list(itertools.filterfalse(vowel,'Aardvark')))    # ['r', 'd', 'v', 'r', 'k']

    # itertools.dropwhile 在迭代对象中筛选，如果遇到第一个不满足条件的值就立即终止筛选，并返回剩余未经过筛选的值列表
    print(list(itertools.dropwhile(vowel,'Aardvark')))  # ['r', 'd', 'v', 'a', 'r', 'k']

    # itertools.takewhile 在迭代中筛选，如果遇到第一个不满足筛选条件的值那么立即终止，并返回已经筛选的值列表
    print(list(itertools.takewhile(vowel,'Aardvark')))  # ['A', 'a']

    # itetrtools.compress 并行处理两个迭代对象，如果后者迭代对象序列中的值为真，那么产出前一个迭代对象中的值列表
    print(list(itertools.compress('Aardvark',(1,0,1,1,0,1))))   # ['A', 'r', 'd', 'a']

    # itertools.islice(it,stop) 或 itertools.islice(it,start,stop,step=1) 产出第一个入参的可迭代对象的切片，相当于s[:stoo] 或 s[start:stop:step]
    print(list(itertools.islice('Aardvark',4))) # ['A', 'a', 'r', 'd'] 相当于 s='Aardvark;s[:4]
    print(list(itertools.islice('Aardvark',4,7)))   # ['v', 'a', 'r'] 相当于s='Aardvark';s[4:7]
    print(list(itertools.islice('Aardvark',1,7,2))) # ['a', 'd', 'a'] 相当于s='Aardvark';s[1:7:2]

# ##########################
# 累计映射itertools.accumulate
# ##########################
    print('-'*20,"累计映射itertools.accumulate",'-'*20)

    samples = [5,4,2,8,7,6,3,0,9,1]
    print('累计求和:',list(itertools.accumulate(samples)))     # [5, 9, 11, 19, 26, 32, 35, 35, 44, 45] 把各项累加产出的和都生成出来
    print('累计筛选最小值:',list(itertools.accumulate(samples,min)))   # [5, 4, 2, 2, 2, 2, 2, 0, 0, 0] 第一次那最开始的两项的值，min进行运算，得到结果，然后后续的各个值得带依次和前面的结果进行min运行，产出所有结果列表
    print('累计筛选最大值:',list(itertools.accumulate(samples,max)))   # 累计筛选最大值: [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]

    import operator
    print('累计乘:',list(itertools.accumulate(samples,operator.mul)))  # 累计乘: [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
    print('range范围累计乘：',list(itertools.accumulate(range(1,11),operator.mul)))   # range范围累计乘： [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

# ##################################################
# 从可迭代对象中生成(序号，数值)的二元组enumerate
# ##################################################
    print('-'*20,"可迭代对象中生成(序号，数值)的二元组itertools.enumerate",'-'*20)
    print(list(enumerate('abcdefg',1))) # 默认编号从0开始，传入的第二个和参数设置开始的序号
    import operator
    print('序列各个项相乘::',list(map(operator.mul,range(11),range(11))))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    print("序列各个项相乘（可迭代对象的长度不同时，按照长度小的为主）",list(map(operator.mul,range(11),[2,4,8])))
    # itertools.starmap(func,it) 把it产出的各个项=作为惨住传递给func，并经过func的处理产出结果，组成结果列表
    print(list(itertools.starmap(operator.mul,enumerate('abcdefg',1))))

    sample = [5,4,2,8,7,6,3,0,9,1]
    print('结合itertools.acculate和enumerate计算累计平均值：',
          list(
              itertools.starmap(
                  lambda a,b:b/a,enumerate(     # 这里a是enumerate产生的元组项的第一项为计数序号，b就是累加的各项的值
                      itertools.accumulate(sample),1
                  )
              )
          )
          )

# ##################################################
# 用于合并的生成器函数itertools.chain
# ##################################################
    print('-'*20,"用于合并的生成器函数itertools.chain",'-'*20)
    # itertools.chain
    print(list(itertools.chain('ABC',range(2))))    # ['A', 'B', 'C', 0, 1]
    print(list(itertools.chain(enumerate('ABC'))))  # [(0, 'A'), (1, 'B'), (2, 'C')]
    print("chain.from_iterable细分数据项:",list(itertools.chain.from_iterable(enumerate('ABC'))))    # [0, 'A', 1, 'B', 2, 'C']
    # zip
    print("zip多项合并,有长度不足的迭代不会继续合并:",list(zip('ABC',range(5),[10,20,30,40])))   #zip多项合并: [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
    print("itertools.zip_longest 对长度较短的迭代填充默认值None：",list(itertools.zip_longest('ABC',range(5))))
    #  [('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)] 用None填充不足的位
    print('itertools.zip_longest 对长度较短的迭代填充设定值？：',list(itertools.zip_longest('ABC',range(5),fillvalue='?')))
#     [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)] 用指定的？填充不足的位


# ##############################
# 惰性计算笛卡尔积itertools.product(产出组合序列)
# ##############################
    print('-'*20,"惰性计算笛卡尔积itertools.product",'-'*20)

    print(list(itertools.product('ABC',range(2))))
    suits = '黑桃 红心 方片 梅花'.split()
    print(list(itertools.product(suits,'AK')))
    # [('黑桃', 'A'), ('黑桃', 'K'), ('红心', 'A'), ('红心', 'K'), ('方片', 'A'), ('方片', 'K'), ('梅花', 'A'),('梅花', 'K')] 组合出A和K的扑克牌花色
    print(list(itertools.product('ABC'))) #[('A',), ('B',), ('C',)] 单个可迭代对象产生一元元组，别是特别有用

    print('设置迭代的元素值的可重复次数',list(itertools.product('ABC',repeat=2)))
#     [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')] 设置repeat值，也就是每个迭代的值可以重复多少次
    print(list(itertools.product(range(2),repeat=3)))
    # [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]

    # repeat参数值可以设置传入的读个迭代对象的各个元素值，每个都重复n次
    rows = itertools.product('AB',range(2),repeat=2)
    for each in rows:
        print(each,end=' ')
        # ('A', 0, 'A', 0) ('A', 0, 'A', 1) ('A', 0, 'B', 0) ('A', 0, 'B', 1) ('A', 1, 'A', 0) ('A', 1, 'A', 1) ('A', 1, 'B', 0) ('A', 1, 'B', 1) ('B', 0, 'A', 0) ('B', 0, 'A', 1) ('B', 0, 'B', 0) ('B', 0, 'B', 1) ('B', 1, 'A', 0) ('B', 1, 'A', 1) ('B', 1, 'B', 0) ('B', 1, 'B', 1)

# ##################################
# 把输入的多项扩充成多个输出项的生成器函数
# ##################################
    print('-'*20,"把输入的多项扩充成多个输出项的生成器函数",'-'*20)
    ct = itertools.count()  # itertools.count是一个无穷循环迭代，不可用list(count())形式，会撑爆能内存
    for i in range(10):
        print(next(ct),end=' ')     # 0 1 2 3 4 5 6 7 8 9
    print()
    print(list(itertools.islice(itertools.count(1,.3),3)))  # [1, 1.3, 1.6] 使用islice先定位范围后，可以创建有限的迭代list
    cy = itertools.cycle('ABC')     #在入参内无限循环迭代
    print(list(itertools.islice(cy,7)))   # ['A', 'B', 'C', 'A', 'B', 'C', 'A'] 只取无限循环迭代的前7个
    print(list(itertools.pairwise(range(7))))   # [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)] pairwise生成当前项和下一项的元组对,前提是下一项存在
    rp = itertools.repeat(7)    # 根据输入重复的产出数据项
    for i in range(5):print(next(rp),end=' ')   # 7 7 7 7 7
    rp2 = itertools.repeat(7,5) # 可以传参限定次数
    print(list(rp2))    # [7, 7, 7, 7, 7] 限定次数以后就可以用list构建列表

    # repeat的作用通常是为函数固定住参数
    print(list(map(operator.mul,range(11),itertools.repeat(5))))    # [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    # 这里使用map，第一个入参迭代产出0-10的数据作为第一个操作数，第二个参数使用repeat持续被不断地产出入参5作为第二个操作数传递给map

    ############
    # 组合生成器 #
    ############
    # itertools.combainations(it,out_len) 把it产出的out_len个项的组合输出
    print(list(itertools.combinations('ABC',2)))    # [('A', 'B'), ('A', 'C'), ('B', 'C')]
    print(list(itertools.combinations_with_replacement('ABC',2)))
    # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
    # 把可迭代对象ABC参数产出两两组合，限定每个可迭代想可以重复两次，因为是组合，所以是无序的

    print(list(itertools.permutations('ABC',2)))    # 产出第一个入参的ABC的两两组成的排列，是有顺序的
    # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

    # permutations和product(产出笛卡尔积)对比，后者使用repeat参数限定项数，而且后者各个分组内的值可以重复
    print(list(itertools.product('ABC',repeat=2)))
    # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]

# ################
# 重新配列元素的生成器
# ################
    print('-'*20,"重新排列元素的生成器",'-'*20)
    # itertools.groupby(it,key=None) 按照分组标准，产出key-val的分局，其中key就是分组标准，不传递key时默认按照迭代重复项作为key
    print(itertools.groupby('LLLLAAGGG'))   # <itertools.groupby object at 0x000001C7516F3C90> 生成器对象
    for k,v in itertools.groupby('LLLLAAGGG'):print(k,'->',v)
    # L -> <itertools._grouper object at 0x00000198E021B970>
    # A -> <itertools._grouper object at 0x00000198E021BA90>
    # G -> <itertools._grouper object at 0x00000198E021B970>

    animals = ['duck','eagle','rat','giraffe','bear','bat','dolphin','shark','lion']
    print('-'*10,'未排序','-'*10)
    for k,v in itertools.groupby(animals,len):print(k,'->',list(v))
    # 4 -> ['duck']
    # 5 -> ['eagle']
    # 3 -> ['rat']
    # 7 -> ['giraffe']
    # 4 -> ['bear']
    # 3 -> ['bat']
    # 7 -> ['dolphin']
    # 5 -> ['shark']
    # 4 -> ['lion']
    # 可迭代对象未经过sort时，使用groupby产出可能有重复项
    animals.sort(key=len)
    print('-'*10,'排序后','-'*10)
    for k,v in itertools.groupby(animals,len):print(k,'->',list(v))
    # 3 -> ['rat', 'bat']
    # 4 -> ['duck', 'bear', 'lion']
    # 5 -> ['eagle', 'shark']
    # 7 -> ['giraffe', 'dolphin']

    print('-'*10,'先reverse再排序','-'*10)
    for k,v in itertools.groupby(reversed(animals),len):print(k,'->',list(v))

    # 7 -> ['dolphin', 'giraffe']
    # 5 -> ['shark', 'eagle']
    # 4 -> ['lion', 'bear', 'duck']
    # 3 -> ['bat', 'rat']

    # #######################
    # 从可迭代对象中产出多个生成器
    # #######################
    print('-'*20,"从可迭代对象中产出多个生成器——tee",'-'*20)
    # itertools.tee(it,n=2) 根据传入的数据，生成n个独立的生成器，n默认为2
    print(list(itertools.tee('ABC')))   # [<itertools._tee object at 0x00000123AC5E96C0>, <itertools._tee object at 0x00000123AC5E9680>] 根据传入的ABC，生成了两个生成器
    g1,g2 = itertools.tee('ABC')
    print(list(g1))     # ['A', 'B', 'C']
    print(list(g2))     # ['A', 'B', 'C']

    # 可以结合zip和tee
    g1,g2 = itertools.tee('ABC')
    print(list(zip(g1,g2))) # [('A', 'A'), ('B', 'B'), ('C', 'C')]

# ###########################
# 读取可得带对象返回单个值的内置函数——all,min.max.reduces,sum等
# ###########################
    print('-'*10,'读取可得带对象返回单个值的内置函数——all,min.max.reduces,sum等','-'*10)

    # all(it) it中每一项都为真，那么返回真，相当于逻辑操作中的与操作,只要有一项是假，那么返回假
    print(all([1,0,3])) # False
    print(all([1,2,3])) # True
    g=(n for n in [0,0.0,7,8])  # False 生成器中有0项,返回False
    print(all(g))

    # Any（it）只要it中有一个为真，那么返回True,相当于逻辑操作中的或,全为假才返回False

    print(any([1,0,3])) #True
    print(any([0,0.0])) # Fasle
    print(any(g))       # True 生成器g中有真值，所以返回True









