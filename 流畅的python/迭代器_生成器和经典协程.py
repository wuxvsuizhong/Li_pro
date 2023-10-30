# 单词序列
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self,text):
        self.text = text
        self.words = RE_WORD.findall(text)  # findall返回字符串列表

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        # repelib.repr函数生成的字符串最多有30个字符，忽略的字符一哦那个...代替
        return 'Sentence(%s)' % reprlib.repr(self.text)


if __name__ == "__main__":
    s = Sentence('"The time has come," the Walrus said')    # Sentence('"The time ha...e Walrus said')
    print(s)
    for word in s:
        print(word)

    print(list(s))  # ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
    print(s[0],s[5],s[-1])  # The Walrus said


# 需要迭代x对象是，python自动调用iter(x)
# 1.调用iter(s)，会检查对象是否实现了__iter__方法，如果实现了就调用它
# 2.如果__iter__没有实现，但是对象实现了__getitem__方法，那么iter()创建一个迭代器，尝试从索引0获取项
# 3.如果上述的尝试失败,抛出TypeError异常，，通常会提示:'C' object is not iterable

# 换言之，只要实现了__iter__或者__getitem__中的任意一个的对象，就是可迭代对象
class Spam:
    def __getitem__(self, i):
        print('->',i)
        raise IndexError()

class GooseSpam:
    def __iter__(self):
        pass

from collections.abc import Iterable
if __name__ == "__main__":
    spam_can = Spam()
    print(iter(spam_can))   # <iterator object at 0x00000206BAF31600>
    print(list(spam_can))   # -> 0
                            # []
    print(isinstance(spam_can,Iterable))    # False 对象如果只实现了__getitem__，虽然可以迭代但是无法通过abc.Iterable的isinstance检查

    print(issubclass(GooseSpam,Iterable))   # True
    goose_spa_can = GooseSpam()
    print(isinstance(goose_spa_can,Iterable))   #True   实现了__iter__方法的对象可以通过abc.Iterable的isinstancea检查

# ####################
# 使用iter()处理可调用对象
# ####################
from random import randint
def d6():
    return randint(1,6)

if __name__ == "__main__":
    d6_iter = iter(d6,1)    # iter传入d6函数后，创造了一个迭代器
    print(d6_iter)  # <callable_iterator object at 0x0000025BC1FBE5C0>
    for roll in d6_iter:
        print(roll)     # 循环抛出随机数，直到抛出的数据为1时，停止迭代


# 使用iter创建可迭代对象的要求是，传入的第一个参数必须是可迭代对象才行，第二个参数是哨兵字符，也就是直到抛出的东西和哨兵字符相等，才会停止迭代
# ###################
# 可迭代对象和迭代器的概念
# ###################
if __name__ == "__main__":
    print('-'*20,"iter创建迭代器",'-'*20)
    s='ABC'
    for char in s:
        print(char)
# 字符串s是一个可迭代对象，它的背后默认有一个迭代器
# 如果可迭代对象没有迭代器，那么使用iter()创建一个得带起，这就是iter的作用
    it = iter(s)
    while True:
        try:
            print(next(it))
        except StopIteration:
            del it
            break

# #########################################################
# 为对象实现__iter__方法(创建对象的迭代器并提供返回对象的迭代器)
# #########################################################

class SentenceIterator:
    def __init__(self,words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self

class SentenceNew:
    def __init__(self,text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'SentenceNew(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return SentenceIterator(self.words)

# 清楚对象的迭代器和可迭代对象这两个概念的差别
# 在这个中，SentenceIterator是SentenceNew对象的迭代器类，iter(SentenceNew("A B C"))调用的就是SentenceNew类实例对象的__iter__方法，从而获取到对象的迭代器，也就是说对象的__iter__方法，返回的是对象的迭代器本身
# 而SentenceIterator作为一个迭代器类型。它需要根据abc.Iterable协议，实现自己的__next__和__iter__,而其__iter__函数，返回SentenceIterator迭代器本身
# 方便的一点是，python提供了yield关键字，从而替代了必须手动实现对象迭代器的做法，更加方便

# #########
# 使用yield
###########
class SentenceNew2:
    def __init__(self,text):
        self.text =- text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f'SentenceNew2(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word

# 只要函数中有yield关键字，那么这个函数就是生成器函数，那么Iter()在调用的时候通过对象的__iter__函数就可以获取到对象的生成器从而实现迭代
# 这里在对象的__iter__函数中，直接在循环中添加yield返回迭代数值

# ########
# 惰性生成器
# ########
# SentenceNew2这个类对象中，有一个self.words的列表，在__init__时，直接把所有的项都生成了，这对于大量数据如果一次性全部生成，不够友好，下面去掉self.words，使用yield在外部需要数据时才返回新的数据

class SentenceLazy:
    def __init__(self,text):
        self.text = text

    def __repr__(self):
        return f'SentenceLazy({reprlib.repr(self.text)})'

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()     # 惰性的返回数据，只有在有新的数据需要时，才返回新数据

# #############
# 惰性生成器表达式
# #############
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')

if __name__ == "__main__":
    print('-'*20,"惰性生成器表达式",'-'*20)

    res1 = [x*3 for x in gen_AB()]
    # 因为gen_AB()的调用，会执行函数中的print
    # start
    # continue
    # end.
    print(res1) # ['AAA', 'BBB']    res1中只有yield返回的值
    for i in res1:
        print('->',i)
    #输出
    # -> AAA
    # -> BBB

    res2 = (x*3 for x in gen_AB())
    print(res2) #<generator object <genexpr> at 0x0000021E49D4C2B0> res2是一个生成器对象，目前还没有具体的值
    for i in res2:
        print('->',i)
    # 输出
    # start
    # -> AAA
    # continue
    # -> BBB
    # end.

# ##############
# 一个等差数列生成器
# ##############
class ArithmeticProgression:
    def __init__(self,begin,step,end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        result_type = type(self.begin+self.step)    ## 这里把begin和step相加，得到的结果获取其类型，作为下一步对begin重新初始化其类型，一些比如int,float,decimal，Fraction混合的类型能通过这样实现类型统一
        result = result_type(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step*index   # 计算数据项

if __name__ == "__main__":
    print('-'*20,"一个等差数列生成器",'-'*20)

    ap = ArithmeticProgression(0,1,3)
    print(list(ap)) #  # [0, 1, 2]
    ap = ArithmeticProgression(1,.5,3)
    print(list(ap)) # # [1.0, 1.5, 2.0, 2.5]
    ap = ArithmeticProgression(0,1/3,1)
    print(list(ap)) # # [0.0, 0.3333333333333333, 0.6666666666666666]
    from fractions import Fraction
    ap = ArithmeticProgression(0,Fraction(1,3),1)
    print(list(ap)) # [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]
    from decimal import Decimal
    ap = ArithmeticProgression(0,Decimal('.1'),.3)
    print(list(ap)) # [Decimal('0'), Decimal('0.1'), Decimal('0.2')]

# #####################
# 等差数列生策划更年期简化版
# #####################
def aritprog_gen(begin,step,end=None):
    result = type(begin+step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result =begin + step*index

# ###################
# itertools生成等差数列
# ###################
import itertools
if __name__ == "__main__":
    print('-'*20,"itertools生成等差数列",'-'*20)
    gen = itertools.count(1,.5) # 鉴于itertlls.count的无线循环特性，这里只获取10次
    for i in range(10):
        print(next(gen))

# itertools.count函数永不停止，如果直接调用list(itertools,count())会创造一个超大列表，直到占满所有内存。在调用失败前，计算机会疯狂运转

# ##########################################################
# itertools.count配合itertools.takewhile控制获取的count获取的次数
# ##########################################################
if __name__ == "__main__":
    print('-'*20,"itertools.count配合itertools.takewhile控制获取的count获取的次数",'-'*20)
    gen = itertools.takewhile(lambda n:n<3,itertools.count(1,.5))   # lambda条件表达式，逗号后的迭代对象会一个个的传递给lambda的入参n
    print(list(gen))    # [1, 1.5, 2.0, 2.5]

# ###############################
# 使用count和takewhile实现的等差数列
# ###############################

def aritprog_gen(begin,step,end=None):
    first = type(begin+step)(begin)
    ap_gen = itertools.count(begin,step)
    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n:n<end,ap_gen)

if __name__ == "__main__":
    print('-'*20,"使用count和takewhile实现的等差数列",'-'*20)
    ap = aritprog_gen(0,.5,10)
    print(list(ap)) # [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]

