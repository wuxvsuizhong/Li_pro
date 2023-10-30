# 大鹅类型的一个基本特征是——即使不继承，也有办法把一个类注册为抽象基类的虚拟子类
from 协议接口和抽象基类__子类化和自定义一个抽象基类 import Tombola
from random import randrange

@Tombola.register
class TomboList(list):  # TomboList继承自list,并且使用Tombola.register注册为Tombola的虚拟子类

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(self)

# python3.3之前，还不能使用register装饰器，需要像下面这样使用冥想的语句注册虚拟子类，但是其实这样的注册方式今天依然可用
# TomboList.register(TomboList)

if __name__ == "__main__":
    print(issubclass(TomboList,Tombola))    # True
    print(issubclass(TomboList,list))       # True
    t = TomboList(range(10))
    print(isinstance(t,Tombola))        # True
    print(isinstance(t,list))           # True

    # 类的继承关系是在一个__mro__的属性中，这个属性的作用就是，按照顺序列出当前类和其超类，python会按照这个顺序搜索方法
    print(TomboList.__mro__)    # (<class '__main__.TomboList'>, <class 'list'>, <class 'object'>)
    # 从结果可以看出，Tombolist继承自list，同时把其注册为Tombola的虚拟子类后，其__mro__属性中列出的超类中没有Tombola,只有list和object

# 注册虚拟子类的方法是在抽象基类上调用register方法。这么做之后，注册的类就变为抽象基类的虚拟子类
# 注册的虚拟子类，issubclass能够识别这种继承关系，但是注册的类不会从抽象基类中继承任何方法或者属性

# 注册虚拟子类看似是把两个原来没有任何关系的类关联起来了，使其有共同的祖先；
# 所以虚拟子类的注册不应该滥用，一定是在类满足某些特性方法的时候，注册为其共性的类的子类，

# 抽象基类的作用最常用于实现名义类型，与之相对的另外一种是 结构类型

# ######################
# 使用抽象基类实现结构类型
# #####################
class Struggle:
    def __len__(self):
        return 10

from collections import abc
if __name__ == "__main__":
    print(issubclass(Struggle,abc.Sized))   # True
    print(isinstance(Struggle(),abc.Sized)) # True

# 这里需要说明的是，没有注册Struugle为任何其他类型的虚拟子类，但是issubclass仍然判断其为abc.Sized的子类
# 这是因为，abc.Sized这个抽象基类，实现了一个 __subclasshook__的方法，当调用issubclass检测Struggle类型是否是abc.Sized的子类的时候，会由abc.Sized这个类的__subclasshook__这个方法去检验，该方法的原型如下：

# class Sized(metaclass=ABCMeta):
#
#     __slots__ = ()
#
#     @abstractmethod
#     def __len__(self):
#         return 0
#
#     @classmethod
#     def __subclasshook__(cls, C):
#         if cls is Sized:
#             return _check_methods(C, "__len__")
#         return NotImplemented

# 可以看到Sized这个类的__subclasshook__就是检验入参的类C中是否含有__len__方法，如果由就返回True
# 也就是说只要一个类有__len__方法，那么它就可以视为abc.Sized的子类

# 可以看出，如果定义了一个抽象基类，并实现了其内部的__subclasshook__方法
# 通过__subclasshook__这个方法，只要其他的类的视线满足这个函数的判断条件，那么就可以把类视为抽象基类的子类
# __subclasshook__这个并不常用，其判断方式过于宽泛

 