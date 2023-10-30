# 切片原理
import operator


class MySeq:
    def __getitem__(self, index):
        return index


s = MySeq()
print(s[1])  # 1
print(s[1:4])  # slice(1, 4, None)
print(s[1:4:2])  # slice(1, 4, 2)
print(s[1:4:2, 9])  # (slice(1, 4, 2), 9)
print(s[1:4:2, 7:9])  # (slice(1, 4, 2), slice(7, 9, None))

# 当类中实现了__getitem__方法后，类就可以表现的像切片一样，可以通过序号，或者下表范围来取固定区域的值

# #################
# 内置的切片类型slice
# #################
print(slice)
print(dir(slice))
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']
# slice的indices属性
# slice.indices接受一个长度len,然后计算序列表示的切片的起始和结尾的索引，以及步长，当超出边界时会被截掉,就像列表的切片一样
print(slice(None, 10, 2).indices(5))  # slice(None,10,2)表示一个切片，.indices(5)计算在只有元素个数为5的序列中，切片范围和步长。语句返回(0, 5, 2) 等同于list[0:5:2]
print(slice(-3, None, None).indices(5))  # (2, 5, 1)  在只有元素个数为5的序列中，逆序-3就是对应的正序的2，这里等同于list[2:5:1]

# ###########################################################################
# 当一个类实现__getitem__和__len__这两个方法后，就可以表现的像切片，可以使用[]切片操作
# ###########################################################################
print('-' * 20, "类实现切片操作", '-' * 20)
from array import array
import reprlib


class Vecter:
    typecode = 'd'  # 类属性

    def __init__(self, components):
        self._components = array(self.typecode, components)  # 类中的_components是array类型

    def __iter__(self):
        return iter(self._components)  # 为了使用_components，构建一个迭代器作为返回值

    def __repr__(self):
        # 被repr()方法调用
        # 使用reprlib.repr对输出的格式进行更加简洁的调整，多余的项显示为...
        components = reprlib.repr(self._components)
        # print("最初的reprlib.repr:",components)    # 最初的reprlib.repr: array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])
        components = components[components.find('['):-1]  # 截取reprlib.repr的结果，拼接自己的格式
        return f'Vecter({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (
                bytes([ord(self.typecode)]) +
                bytes(self._components)
        )

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        """对n维坐标取模"""
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def fromybtes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)  # 这里不用*memv的原因是本身Vecter的类初始化__init__接受的就是可迭代的序列components

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        print("calling parent getitem")
        return self._components[index]


v1 = Vecter([3, 4, 5])
print(v1[0], v1[-1])  # 3.0 5.0
v7 = Vecter(range(7))
print(v7[1:4])  # array('d', [1.0, 2.0, 3.0])
# 因为内置的_components的类型是array类型，所以切片出来的类型表现就是是array
# 下面将切片返回的类型转为Vecter类本身的类型

# ##################
# 切片转为Vecter类型
# ##################
print('-' * 20, "切片转为Vecter类型", '-' * 20)


# 定义NewVecter继承自Vecter,重写__getitem__方法
class NewVecter(Vecter):

    def __init__(self, components):
        super(NewVecter, self).__init__(components)
        # self._components = array(self.typecode,components)  # 类中的_components是array类型

    def __getitem__(self, key):
        if isinstance(key, slice):
            # 如果key是切片类型
            cls = type(self)  # 获取实例的类
            return cls(self._components[key])  # 然后调用类的构造函数构建新的实例NewVecter
        # key是单个的序号
        index = operator.index(key)
        return self._components[index]


v7 = NewVecter(range(7))
print(v7)  # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
print(v7[1:4])  # (1.0, 2.0, 3.0)
print(repr(v7[
           1:4]))  # Vecter([1.0, 2.0, 3.0])     调用重写的__getitem__方法，当传入的参数是一个切片的时候，构建一个新的Vecter（因为没有重写__repr__方法，所以调用的是父类的__repr__，显示就是Vecter类型而不是NewVecter)

print(repr(v7[-1:]))  # Vecter([6.0]) 长度为1的切片也创造一个Vecter实例
# print(v7[1,2])  # TypeError: 'tuple' object cannot be interpreted as an integer Vecter不支持多维索引，所以索引元组或者多个切片就会报错


# ##################
# 控制属性的动态存取
# ##################
v = NewVecter(range(10))
# print(v.x)    # AttributeError: 'NewVecter' object has no attribute 'x'

# 因为n维向量Vecter中并没有诸如x，y，z这样的成员属性，所以直接获取会报错
# 我们可以间接通过__match_args__，让Vecter类型支持位置模式匹配，来间接访问属性

print('-' * 20, "控制属性的动态存取", '-' * 20)


class NewVecter3(Vecter):
    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        super(NewVecter3, self).__init__(components)

    def __getattr__(self, name):
        cls = type(self)
        try:    #其实就是通过__match_args__做了做了一个属性名和位置的映射
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos <= len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} 对象中没有属性 {name!r}'
        raise AttributeError(msg)


v = NewVecter3(range(5))
print(f'{v!r}')  # Vecter([0.0, 1.0, 2.0, 3.0, 4.0])
print(v.x)  # 0.0   # 因为实现了__getattr__方法，所以'x'属性映射到了_components的0位置序号
# 本意是通过这个映射关系能设置实例v的属性值
v.x = 10  # 为Vecter的实例v设置属性x的值为10
print(v.x)  # 10
print(f'{v!r}')  # Vecter([0.0, 1.0, 2.0, 3.0, 4.0])


# 即使v.x能设置属性x,但是仍然无法修改实例v中的属性值，这里是因为获取实例属性和设置实例属性时是两回事
# 获取实例属性v.x是通过__match_args__的映射关系获取到了_components的序号0位置的元素
# 但是设置属性的时候，会直接为实例绑定新的属性名和属性值 v.x=10，再次访问v.x就有了该属性，就不会调用__getattr__方法
# __getattr__是当实例没有属性的时候才会去调用的
# 为了防止能设置实例v.x属性但是实际又没有在vecter中生效的矛盾现象，需要控制设置属性时的行为，让v.x成为只读，设置属性时直接抛出异常

print('-' * 20, "控制属性的动态存取,(添加__setattr__禁止为特定的属性赋值)", '-' * 20)

class NewVecter4(NewVecter3):
    def __init__(self, components):
        super(NewVecter3, self).__init__(components)

    def __setattr__(self, name: str, value):
        """控制不能设置实例的属性名为a~z的属性"""
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = '只读的属性 {attr_name!r}'
            elif name.islower():
                error = "不能在类 {cls_name} 中设置'a'-'z'属性"
            else:
                error = ''
            if error:
                msg = error.format(cls_name = cls.__name__,attr_name = name)
                raise AttributeError(msg)
        super().__setattr__(name,value)

v = NewVecter4(range(5))
print(f'{v!r}') # Vecter([0.0, 1.0, 2.0, 3.0, 4.0])
print(v.x)  # 0.0
v.X = 100   # 可以添加成功，因为属性名不在a-z范围内
print(f'{v!r}') #Vecter([0.0, 1.0, 2.0, 3.0, 4.0])
# v.x = 10    # error AttributeError: 只读的属性 'x'
