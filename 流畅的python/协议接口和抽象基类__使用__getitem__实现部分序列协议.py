class Vowelas:
    def __getitem__(self, i):
        return 'AEIOU'[i]

v = Vowelas()
print(v[0]) # A
for c in v:print(c)
# 输出
# A
# E
# I
# O
# U


# 只要实现__getitem__方法，就可以按照序列来获取索引项，以支持迭代和in运算符
# 完全实现一个协议可能需要实现多个方法，但是通常只实现部分协议方法


from random import shuffle
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = '黑桃 方块 梅花 红桃'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        # 定义了__len__后，在外部就可以使用len()方法长度个数
        return len(self._cards)

    def __getitem__(self, position):
        # 自定义__getitem__的行为是取_cards列表中的序号对应的元素
        return self._cards[position]


deck = FrenchDeck()
try:
    shuffle(deck)      # 使用这个可以打乱序列中的元素顺序，进行洗牌
except Exception as e:
    print(e)

#     x[i], x[j] = x[j], x[i]
#     ~^^^
# TypeError: 'FrenchDeck' object does not support item assignment
# 有了__getitem__以后，可以使用obj[n]用过下标访问对象中的数据，但是无法重新设置，访问对象的数据和设置对象的数据是两回事
# 因为shuffle在打乱顺序的时候会对序列元素的位置进行交换，会重新赋值，需要对象有相应的赋值方法,也就是对象需要有__setitem__

# ###########################################
# 给FrenchDeck 类打上猴子补丁，以便内能够实现洗牌功能
# ###########################################
def set_card(deckobj,position,card):
    deckobj._cards[position] = card
FrenchDeck.__setitem__ = set_card

print("洗牌前：",deck[:5])
shuffle(deck)
print("洗牌后：",deck[:5])
# [Card(rank='K', suit='梅花'), Card(rank='10', suit='黑桃'), Card(rank='2', suit='红桃'), Card(rank='8', suit='方块'), Card(rank='K', suit='黑桃')]

# 注意看这里做了什么能够让原本不支持洗牌的类型变为支持洗牌的类型？
# 1.定义一个函数set_card,这个函数有三个参数，依次为FrenchDeck对象deckobj，序号position,Card类型的对象card
# 2.FrenchDeck.__setitem__ = set_card ，给类FrenchDeck动态的添加__setitem__方法
# 然后就可以对FrenchDeck的实例deck进行洗牌操作了

# 这里的set_card就是所谓的“猴子补丁”
# 猴子补丁的方便之处在于，当我们引用一个第三方模块的时候，需要新增某个功能时，不需要去修改源码，直接动态地为对象(类)添加方法
# 添加的补丁函数的入参需要和类的"接口"函数的入参位置以及含义一致，如__setitem__在类中的原型是 __setitem__(self,key,value).那么self对应的就是实例对象本身，key和value分别是要给对象里的通过key获取的元素赋值value，所以添加的补丁set_card的参数的顺序deckobj,position,card


