items=[
    (1,'a'),
    (2,'b'),
    (3,'c'),
    (4,'e'),
    (5,'f'),
    (3,'cc'),
    (1,'aa')
]

index = {}
for key,val in items:
    # setdefault(key,val)作用是设置字典的默认值，当字典中key不存在时，在字典中自动设置key:val键值对
    # setdefault返回的是设置后的value的引用
    index.setdefault(key,[]).append(val)

# index.setdefault(key,[]) 当index中没有key时，设置键key，并把其值设置为一个list
print(index)  # {1: ['a', 'aa'], 2: ['b'], 3: ['c', 'cc'], 4: ['e'], 5: ['f']}

################################################
# 使用collections.defaultdict代替dict.setdefault
################################################
from collections import defaultdict
# 初始化一个defaultdict并设置其默认value为list
default_index = defaultdict(list)
for key,val in items:
    # defualtcidt的特性就是当key不存在的时候，会自动为键key设置默认值
    default_index[key].append(val)
print(default_index)
