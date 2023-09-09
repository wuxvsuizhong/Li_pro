import collections

# 关于__len__和魔术方法__getitem__的使用

Card = collections.namedtuple('Card', ['rank', 'suit'])


# nametuple的作用就是可以创建只有属性没有自定义方法的简单类对象
# 这里nametuple('Card',['rank','suit'])第一个参数是类名，第二个参数是一个列表，表示这个Card类拥有的属性有rank和suit

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


print("Card自定义一张牌")
beer_card = Card('7', '方块')
print(beer_card)

print("获取deck长度数量")
deck = FrenchDeck()
print(len(deck))  # 会调用FrenchDeck中的__len__方法

print('按序号随机获取两张牌')
print(deck[0])  # deck[n]会调用__getitem__方法
print(deck[-1])

print("遍历所有的牌")
for i in range(len(deck)):
    print(deck[i])

print("随机抽取一张牌")
from random import choice

# choice，随机从可迭代的序列中抽取一个元素(按int序号)
print(choice(deck))
print(choice(deck))
print(choice(deck))

# 因为有__getitem__实现了FrenchDeck类的[]操作符，可以像切片一样操作deck
print("deck的切片操作")
print(deck[:3])
# list[start:end:step]
print(deck[12::13])
print('把deck逆序')
for card in reversed(deck):
    print(card)

# 自定义的排序方式
suit_value = dict(黑桃=4, 方块=3, 梅花=2, 红桃=1)
def spades_high(card):
    # 通过得到的点数计算牌面大小，2-A的序号算做牌面的值，suit_value花色登记值为每单个牌面值的点数，则总的点数 = 牌面值*花色代表的点数
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value*suit_value[card.suit]
print("对deck排序")
# 这里通过设置spades_high计算获取deck牌面的登记，用作内置sorted函数进行运算比较，然后排列
for card in sorted(deck,key=spades_high):
    print(card)

