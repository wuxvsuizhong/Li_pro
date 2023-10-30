import random
from collections import namedtuple,abc
from random import shuffle

卡片 = namedtuple("扑克牌",['大小','花色'])
class FrechDeck2(abc.MutableSequence):
    大小顺序集 = [str(n) for n in range(2,11)] + list('JQKA')
    花色集 = '梅花 方片 黑桃 红心'.split()

    def __init__(self):
        self._cards = [卡片(大小,花色) for 大小 in self.大小顺序集 for 花色 in self.花色集]

    def __len__(self):
        # 抽象基类abc.MutableSequence的抽象方法，需要实现
        return len(self._cards)

    def __getitem__(self, position):
        # 抽象基类abc.MutableSequence的抽象方法，需要实现
        return self._cards[position]

    def __setitem__(self, position, value):
        # 抽象基类abc.MutableSequence的抽象方法，需要实现
        self._cards[position] = value

    def __delitem__(self, position):
        # 抽象基类abc.MutableSequence的抽象方法，需要实现
        del self._cards[position]

    def insert(self, index, value):
        # 抽象基类abc.MutableSequence的抽象方法，需要实现
        self._cards.insert(index,value)

if __name__ == "__main__":
    deck = FrechDeck2()
    print('洗牌前:',deck[:5])
    shuffle(deck)
    print('洗牌前:',deck[:5])

    print(dir(FrechDeck2))
    # ['__abstractmethods__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__iadd__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', 'append', 'clear', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', '大小顺序集', '花色集']

# 除了FrenchDeck2自身重新的方法外，以及必须要实现的抽象方法之外，FrechDeck2从抽喜基类abc.MutableSequence 获得了'append', 'clear', 'count', 'extend', 'index'。'pop', 'remove', 'reverse'等方法

# 抽象基类是一种协议接口的协议约定
# 继承抽象基类必须要实现抽象基类中的抽象方法
if __name__ == "__main__":
    print(isinstance(deck,abc.MutableSequence)) #True
    print(issubclass(FrechDeck2,abc.MutableSequence))   #True

# 只要继承并实现了抽象基类中的抽象方法，那么就可以用isinstance和issubclass来判断实力对象和类是否是某个抽象基类的子类

# ######################
# 自定义一个抽象基类
# ######################
# 基本不好建议自定义抽象基类，标准库里面的抽象基已经基本满足99&的场景

import abc

class Tombola(abc.ABC):     # 继承abc.ABC定义一个抽象基类

    @abc.abstractmethod     # 庄装饰器设置方法为抽象方法
    def load(self,iterable):
        """从迭代对象中添加元素"""

    @abc.abstractmethod
    def pick(self):
        """随机删除元素，再返回被删除元素,如果实例为空，赢应抛出LookupError"""

    def loaded(self):
        """如果至少有一个元素，就返回True,否则返回False"""
        return bool(self.inspect())

    def inspect(self):
        """返回由容器中的当前元素构成的有序元组"""
        items = []
        while True:
            # 调用self.pick随机从实例中取。直到取完，取出来的数据放在临时items中
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)    # 再把取出的数据放回去
        return tuple(items)

# ##################
#子类化自己定义的抽象基类
# ##################

class Fake(Tombola):
    """一个没有完全实现父抽象基类的子类"""
    def pick(self):
        return 13
if __name__ == "__main__":
    print(Fake)     # <class '__main__.Fake'>
    # f = Fake()
    # TypeError: Can't instantiate abstract class Fake with abstract method load
    # 从错误了可以看出，没有完全实现父抽象基类的继承，是失败的，无法实例化

class BingoCage(Tombola):
    def __init__(self,items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self,items):
        # 实现父抽象基类的抽象方法
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        # 实现父抽象基类的抽象方法
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()


# ######################################
#子类化自己定义的抽象基类——重写父类的方法
# ######################################
class LottoBlower(Tombola):

    def __init__(self,iterable):
        self._balls = list(iterable)

    def load(self,iterable):
        # 实现父抽象基类的抽象方法
        self._balls.extend(iterable)

    def pick(self):
        # 实现父抽象基类的抽象方法
        try:
            posision = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LottoBlower')
        return self._balls.pop(posision)

    def loaded(self):
        # 重写父类的方法
        return bool(self._balls)

    def inspect(self):
        # 重写父类的方法
        return tuple(self._balls)



