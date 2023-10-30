import fractions
import itertools
import math

from 序列的特殊方法__哈希_等值测试_格式化 import Vecter
# ###################
# 重载加法运算符__add__
# ###################

class Vecter(Vecter):
    def __init__(self,componets):
        super().__init__(componets)

    def __abs__(self):
        return math.hypot(*self)

    def __neg__(self):
        """一元取反运算符，构建一个新的Vecter把每个分量都取反"""
        return Vecter(-x for x in self)

    def __pos__(self):
        """一元取正运算符，构建一个新的Vecter，每个分量保持不变"""
        return Vecter(self)

    def __add__(self, other):
        pairs = itertools.zip_longest(self,other,fillvalue=0.0)
        # pairs是一个生成器，会生成(a,b)形式的元组，a来自self,b来自other,如果两者的长度不同，那么可以使用fillvalue的值填充较短的一方的缺少的值
        return Vecter(a+b for a ,b in pairs)    # 返回一个新的实例，没有改变self和other

if __name__ == "__main__":
    v1 = Vecter([3,4,5,6])
    v2 = Vecter([1,2])
    print(v1+v2)    # (4.0, 6.0, 5.0, 6.0)
    print(v1+v2 == Vecter([3+6,4+7,5+8]))   #False
    print(v1+(10,20,40))    # (13.0, 24.0, 45.0, 6.0)   从__add__得分 的原型看，只只要是可迭代的数据，就可以与Vecter相加

    # (10,20,30)+v1     TypeError: can only concatenate tuple (not "Vecter") to tuple
#    “+”操作默认只调左侧的数据的__add__方法， 因为左侧的数据类型是元组，不是Vecter，没有__add__方法，
#    要想让类型实现"+"不论在哪个位置，都能够调进行相加操作，Vecter需要实现__radd__


#   对于表达式a+b,python为中缀运算符提供了特殊的分配机制
#   1.如a有__add__方法，而且不返回NotImplemented,那么就调用a.__add__(b),返回结果
#   2.如果a没有__add__方法，或者调用__add__方法返回NotImplemented,就检查b有没有__radd__方法，如果有，而且不返回NotImplemented，就调用b.__radd__(a)，返回结果
#   3.如果b没有__radd__方法，或者调用__radd__方法返回NotImplemented,就抛出TypeError,并在错误消息中指明不支持操作类型

# ############################
# 实现加法运算符的反向方法__radd__
# ############################

class Vecter(Vecter):
    def __init__(self,componets):
        super().__init__(componets)

    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self,other,fillvalue=0.0)
            return Vecter(a+b for a,b in pairs)
        except TypeError:
            return NotImplemented   # 返回说明不支持的操作

    def __radd__(self, other):
        return self+other


if __name__ == "__main__":
    print('-'*20,"添加__radd__运算符",'-'*20)
    v1 = Vecter([1,2,3,4])
    v2 = (10,20,30)+v1
    print(v2)   #(11.0, 22.0, 33.0, 4.0)    实现了__radd__操作后，Vecter就可以放在"+"操作符的后面
#    因__add__的实现是，只要Vecter和一个可迭代的类型相加即可，

    # v1+1  #单独的1不是可迭代对象，所以TypeError: 'int' object is not iterable
    # v1+'abc' # abc字符串最燃可以迭代，但是__add__方法中，不支持字符串和int相加，TypeError: unsupported operand type(s) for +: 'float' and 'str'

# ##########
# 实现’*‘运算符
# ##########
class Vecter(Vecter):
    def __init__(self,componets):
        super().__init__(componets)

    def __mul__(self, scalar):
        return Vecter(n * scalar for n in self)

    def __rmul__(self, scalar):
        return self*scalar


    def __mul__(self,scalar):
        """改进的__mul__，要求scalar能够转换为float，否则返回操作不支持"""
        try:
            factor = float(scalar)
        except TypeError:
            return NotImplemented
        return Vecter(n*scalar for n in self)


if __name__ == "__main__":
    print('-'*20,"重载*运算符",'-'*20)

    v1 = Vecter([1,2,3])
    print(v1*10)    # (10.0, 20.0, 30.0)    Vecter和证书相乘
    print(v1*True)  # (1.0, 2.0, 3.0)   Vecter和bool相乘
    print(v1*fractions.Fraction(1,3))   # (0.3333333333333333, 0.6666666666666666, 1.0) Vecter和分顺相乘

# ##############
# 举实矩阵乘法运算@
# ##############
from collections import abc
class Vecter(Vecter):
    def __matmul__(self, other):
        if isinstance(other,abc.Sized) and isinstance(other,abc.Iterable):
            if len(self) == len(other):
                return sum(a*b for a,b in zip(self,other))
            else:
                raise ValueError('@ 需要两个Vecter的分量数量相同')
        else:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other

if __name__ == "__main__":
    print('-'*20,"重载@运算符",'-'*20)

    va = Vecter([1,2,3])
    vb = Vecter([5,6,7])
    print(va@vb)    #38.0 相当于 1*5 + 2*6 + 3*7
    print([10,20,30]@va)    # 140.0 相当于10*1 + 20*2 + 30*3

    v1 = Vecter([1.0,2.0,3.0])
    print(v1 == (1,2,3))    #True
    # 基于Vecter的__eq__方法的实现如下：
    # def __eq__(self, other):
    #     return len(self) == len(other) and all(a == b for a,b, in zip(self,other))
    # 也就是先判断Vecter实例本身的数据维度是否和other相等，如果相等，那么，进一步的判断Vecter实例的每一个数据维度的值是否和other可迭代对象的每一项的值相等，如果都满足那么说明相等
    # 还显然，这种相等方式的判断是不够全面的，因为"任意的可迭代对象"不一定是Vecter类型，简单粗暴的这样比较是不对的


# #################
# 比较运算符
# #################
class Vecter(Vecter):
    def __eq__(self, other):
        """优化的__eq__，先判断other是否是Vecter类型"""
        if isinstance(other,Vecter):
            return len(self) == len(other) and all(a == b for a,b in zip(self,other))
        else:
            return NotImplemented   # 如果不是Vecter类型，返回操作不支持的报错


if __name__ == "__main__":
    print('-'*20,"重载==运算符",'-'*20)

    v1 = Vecter([1.0,2.0,3.0])
    print(v1 == (1,2,3))    # False
    print(v1 == Vecter((1,2,3)))    # True 类型相同才判断相等

# python的==判断后有一些几个流程：
# 1. a==b,会先调用a.__eq__(b),如果有返回值，那么直接去这个返回值作为比较结果，如果返回NotImplemented,那么会尝试调用 b.__eq__(a)
# 2. 如果b.__eq__(a)有返回值，那么取这个返回值作为比较结果，如果返回NotImplementted.那么会尝试调用对象ID比较，做最后的判断

# 只要实现了__eq__方法，那么!= 操作就无需要再实现了，因为原始祖类object的__ne__方法已经实现了对__eq__方法的取反操作实现

# #####################
# 增量赋值(就地计算)运算符号
# #####################
if __name__ == "__main__":
    print('-'*20,"增量赋值",'-'*20)

    v1 = Vecter([1.0,2.0,3.0])
    print(f'{v1!r}')    # Vecter([1.0, 2.0, 3.0])

    v1_cp = v1
    print(id(v1))   # 2249883273872

    v1+=Vecter([4,5,6])
    print(f'{v1!r}')    # Vecter([5.0, 7.0, 9.0])
    print(id(v1))   # 2249883274256
    print(id(v1_cp))    # 2249883273872

    v1*=11
    print(f'{v1!r}')    # Vecter([55.0, 77.0, 99.0])
    print(id(v1))       # 2249883274128

#     通过+=,*=操作符前后，对比v1的id值，可以发现，在类没有实现增量赋值运算符重载的情况下，pthon默认为类实现的增量操作运算是创建了一个新的数据对象，如 a+=b 和 a=a+b是相同的
# 如果实现了__iadd__方法，那么，a+=b就会调用就地运算的方法，不会创建新的对象，
# 但是需要注意的一点是，不可变类型不能实现就地运算
# ############
# 就地运算符重载
# ############
from 协议接口和抽象基类__子类化和自定义一个抽象基类 import Tombola,BingoCage
class AddableBingoCage(BingoCage):
    def __add__(self, other):
        if isinstance(other,Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other,Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                msg = ('+=操作的右操作数必须是Tombola类或者是iterable(可迭代的)')
                raise TypeError(msg)
        self.load(other_iterable)
        return self     # 重要提示，可变对象的增量赋值运算符必须返回self,

if __name__ == "__main__":
    print('-'*20,"就地运算符重载",'-'*20)

    vowels = "AEIOU"
    globe = AddableBingoCage(vowels)
    print(globe.inspect())  # ('I', 'U', 'A', 'E', 'O')
    print(globe.pick() in vowels)   # True
    print(len(globe.inspect())) # 4
    globe2 = AddableBingoCage('XYZ')
    globe3 = globe + globe2
    print(len(globe3.inspect()))    # 7

    globe_orig = globe
    print(len(globe.inspect())) # 4
    print(globe.inspect())  # ('E', 'A', 'O', 'I')
    print(globe2.inspect()) # ('Z', 'X', 'Y')
    print(id(globe))    # 2600209045136
    globe += globe2
    print(globe.inspect())  # ('Y', 'U', 'E', 'X', 'A', 'Z', 'I')
    print(id(globe))    # 2600209045136

    globe += ['M','N']
    print(globe.inspect())  # ('U', 'Z', 'X', 'Y', 'E', 'A', 'N', 'M', 'O')
    print(id(globe))    # 2600209045136


