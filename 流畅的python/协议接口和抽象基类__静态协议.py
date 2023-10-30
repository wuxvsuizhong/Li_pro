# 一个静态协议的简单例子
from __future__ import annotations

def double(x):
    """一个返回入参的2倍的值的方法"""
    return x * 2

# 如需要为double函数添加注解，那么注解其入参的类型和返回值的类型就会是一个难题
# 从函数的原型可以看出，double函数的入参是需要能够支持'*'运算的这种类型，那么如何通过注解来说明这样一种类型？
# 由此引出“协议”

# ##################
# 静态协议的引入
# ##################

from typing import TypeVar,Protocol

# 使用TypeVar定义一种类型
T = TypeVar('T')

class Repeatable(Protocol):    #类继承自Prortocal
    def __mul__(self:T, repeat_count: int)-> T:...  # Repeatable类有__mul__方法

# TypeVar设定一种类型，这种类型的行为需要支持Repeatable 中规定的东西
RT = TypeVar('RT',bound=Repeatable)

def double(x:RT) ->RT:
    return x*2

class A:
    def __init__(self):
        pass


# print(double(A()))
#     return x*2
#            ~^~
# TypeError: unsupported operand type(s) for *: 'A' and 'int'
# 因为A这个自定义的类，没有实现__mul__方法，所以，它无法被double函数调用

class B:
    def __init__(self):
        pass

    def __mul__(self, other):
        return 'BB'

print(double(B()))  # BB
# B这个类的之所以可以顺利被double作为入参，并顺利获取返回值，是因为B这个类实现了__mul__
# 当某个方法或者函数需要的参数类型或者是返回值是需要支持某种行为的特定类型的时候，就需要用协议来定制一种类型，然后通过这种类型去代表这种塔顶类型，这是就需要使用协议

# #####################################################
# 另外一个协议的例子——typing.SupportsComplex 协议的视线和使用
# #####################################################
# --------------------typing.SupportsComplex协议的原型如下：
# @runtime_checkable
# class SupportsComplex(Protocol):
#     """An ABC with one abstract method __complex__."""
#
#     __slots__ = ()
#
#     @abstractmethod
#     def __complex__(self) -> complex:
#         pass

# SupportsComplex这个标准库中的协议只有一个抽象方法，限定只要对象实现了__complec__方法，而且只接受self参数，并返回一个complec值，那么说明该对象就支持SupportsComplex协议。称为该对象和协议SupportsComplex“相容”



from typing import SupportsComplex
import numpy as np

c64 = np.complex64(3+4j)
print(isinstance(c64,SupportsComplex))  # True  复数类型c64实例和SupportsComplex相容
c = complex(c64)
print(f'{c!r}')     # (3+4j)
print(isinstance(c,SupportsComplex))    # True  复数类型c实例和SupportsComplex相容
print(complex(c))   # (3+4j)

# 使用Protocal添加的注解类型，可以被mypy静态检查工具检测，如果在代码中参数类型不符合Protocal的限定，那么mypy会泡池异常

# ######################################################################################
# 改造Vecter2d类型，使其和SupportComplex相容——为其实现SupportsComplex协议中的方法
# ######################################################################################
from 符合python风格的对象__向量类升级版 import Vecter2d

# 没有实现__complex__之前，Vecter2d类型的实例是和SupportsComplex不相容的
print(isinstance(Vecter2d(3,4),SupportsComplex))    # False

class NewVector(Vecter2d):
    def __init__(self,x,y):
        super().__init__(x,y)

    def __complex__(self) ->complex:    # 为函数添加注解，其返回值是complex类型
        """只是为了能够让NewVector能够把复数转换为向量"""
        return complex(self.x,self.y)

    @classmethod
    def fromcomplex(cls,datnum:SupportsComplex) -> NewVector:
        # 给函数入参添加注解，datnum入参需要是和SupportsComplex相容，返回值是一个NewVector类型
        # 注意这里NewVector还没有完成定义，所以需要导入__futrue__.annotations，否则使用其作类型注解会报错
        c = complex(datnum)     # 这里做complex转换是为了能够在下一步引用complex类型的real和imag
        return cls(c.real,c.imag)

# 实现了__complex__之后。NewVector就可以和SupportsComplex相容
print(isinstance(NewVector(3,4),SupportsComplex))    # True

# #######################
# 设计一个自己的静态协议
# #######################
from typing import Protocol,runtime_checkable,Any,Iterable
from typing import TYPE_CHECKING
import random

# 设计一个协议class，用于限定类型对象需要实现pick方法，方法的入参为self,返回值暂定为任何类型Any
@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any: ...

# 以之前的Tonbola类为参照，定义了如下的SimplePicker类
class SimplePiker:
    def __init__(self,items:Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) ->Any:
        return self._items.pop()


def test_isinstance() -> None:
    popper:RandomPicker = SimplePiker([1])
    # popper是一种和RandomPicker协议相容的类型，它被赋值为SimplePiker类的实例
    assert isinstance(popper,RandomPicker)
    # 断言poopper最终的类型是和RandomPicker相容的

def test_item_type()->None:
    items = [1,2]
    popper = SimplePiker(items)
    item = popper.pick()
    assert item in items
    if TYPE_CHECKING:
        reveal_type(item)
    assert isinstance(item,int)

# 对于这部分的检查，mypy只有一个提示 协议接口和抽象基类__静态协议.py:141: note: Revealed type is "Any"

# ######################
# 扩展一个协议
# ######################
# 如果在实际的使用中，需要协议需要多个方法，那么不要直接为协议添加方法，最好是衍生原协议，创建一个新协议
# 以上面的RandomPicker协议为基础，扩展另外一个协议LoadableRandomPicker

from typing import runtime_checkable,Protocol

@runtime_checkable
class LoadableRandomPicker(RandomPicker,Protocol):
    # LoadableRandomPicker 从RandomPOicker扩展而来，它除了继承了父类协议的pick方法之外。，是扩展要求类型需要定义load方法
    def load(self,Iterable)->None:...

from 协议接口和抽象基类__子类化和自定义一个抽象基类 import BingoCage

def test_isinstance2():
    print(isinstance(BingoCage(range(5)), LoadableRandomPicker))    # True
    # BingoCage实现了load和pick方法，所以和LoadableRandomPicker相容的

    popper:RandomPicker = SimplePiker([1])
    # # popper是一种和RandomPicker协议相容的类型，它被赋值为SimplePiker类的实例
    assert isinstance(popper,RandomPicker)
    # # 断言poopper最终的类型是和RandomPicker相容的

    print(isinstance(popper,LoadableRandomPicker))  # False
    # popper只有pick方法吗，没有load方法，所以不能和 LoadableRandomPicker相容


# 总结：静态协议其实是一种对具有某种特性方法的类型的高度抽象归纳，把实现了某个方法的类型统统归纳为一种协议类型
# 其作用其实和抽象基类非常类似，静态协议可以限定类型的行为，当类型拥有协议中的方法时，就判定类型和协议是相容的
# 当类型和协议相容时，就可以用协议类型来替代诸多具体的类型，把协议类型作为一种泛型来使用，实现类型注解的"  多态"
# 定义静态协议，需要继承自typing.Protocal类
# 如果需要扩展协议类的方法，那么不要直接在原协议类中增加方法，而是采用继承，同时新的协议类也要同时添加Ptotocal的继承（Protocal和原协议类作为新的协议类的超类被同事继承)
# 使用静态协议为可以为函数或者类型添加更加详细的注解，同时能被mypy检查通过