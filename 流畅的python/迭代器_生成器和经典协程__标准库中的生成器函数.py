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











