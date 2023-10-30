import functools
import itertools
import operator
from array import array
import reprlib,math

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
        """这个版本的__eq__在对比多维向量Vecter时，会创建庞大的tuple元组，效率会下降"""
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



if __name__ == "__main__":
    v1 = Vecter([1,2])
    t1 = (1,2)
    print(v1 == t1)     # True
    # 这里的比较是存在问题的，t1的类型是元组并不是Vecter，所以严格来说t1和v1并不相等，需要后续优化__eq__逻辑

class NewVecter(Vecter):
    def __init__(self,components):
        super(NewVecter,self).__init__(components)

    def __eq__(self,other):
        # 相比于基类Vecter的版本的__eq__，这里的效率更更高
        if len(other) != len(self):
            return False
        for a,b in zip(self,other):
            if a != b:
                return False
        return True

    def __hash__(self):
        """使用reduce规约函数，累计地计算向量各个维度的异或结果"""
        hashes = (hash(x) for x in self._components)
        # 使用reduce规约函数，函数的额第三个参数是当迭代的序列为空时返回该值，否则，在规约累计的一开始，以改值作为第一个参数
        return functools.reduce(operator.xor, hashes, 0)

    def __eq__(self,other):
        """最新版的__eq__函数，使用and逻辑与判断两边的条件都需要满足"""
        return len(self) == len(other) and all(a == b for a,b in zip(self,other))
        # all()函数，判断迭代分量的各项的值都是True是才返回True,只要有一项是False那么就返回False

if __name__ == "__main__":
    v1 = Vecter([1,2])
    t1 = (1,2)
    print(v1 == t1)     # True

# #############
# 最终版的Vecter
# #############
# 在原来的基础上，当向量Vecter的维度超过2维的时候，就是球坐标，当Vecter支持n个维度的时候（超过4维)，就是超球体
# 再这里仅仅实现当坐标为4维的时候，使用球坐标格式format
class Vecter:
    typecode = 'd'

    def __init__(self,components):
        self._components = array(self.typecode,components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        compoents = reprlib.repr(self._components)
        compoents = compoents[compoents.find('['):-1]
        return f'Vecter({compoents})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)])+bytes(self._components)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a,b, in zip(self,other))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor,hashes,0)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key,slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

    __match_args__ = ('x','y','z','t')

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0<= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} 对象中没有属性 {name!r}'
        raise AttributeError(msg)

    def angle(self,n):
        """使用n维球体的公式，计算挪个角坐标"""
        r = math.hypot(*self[n:])
        a = math.atan2(r,self[n-1])
        if (n == len(self)-1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        """创建生成器表达式，按需计算所有的角坐标"""
        return (self.angle(n) for n in range(1,len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # 超球面坐标
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)],self.angles()) # 使用otertools.chain函数生成 生成器表达式，无缝迭代向量的模和各个角坐标
            outer_fmt = '<{}>'  # <>显示球面坐标
        else:
            coords = self
            outer_fmt = '({})'  #()显示笛卡尔坐标
        components = (format(c,fmt_spec) for c in coords)   # 按需格式化各个坐标分量
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls,octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

if __name__ == "__main__":
    # 使用可迭代对象创建Vectrer实例
    print(Vecter([3.1,4.2]))
    print(Vecter((3,4,5)))
    print(Vecter([3,4,5]))
    print(Vecter(range(10)))

    # 输出
    # (3.1, 4.2)
    # (3.0, 4.0, 5.0)
    # (3.0, 4.0, 5.0)
    # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0)

    # 测试二维向量
    print('-'*20)
    v1 = Vecter([3,4])
    x,y = v1
    print(x,y)
    print(f'{v1!r}')
    v1_clone = eval(repr(v1))
    print(v1 == v1_clone)
    print(v1)
    octets = bytes(v1)
    print(octets)
    print(abs(v1))
    print(bool(v1),bool(Vecter([0,0])))

    # 输出
    # 3.0 4.0
    # Vecter([3.0, 4.0])
    # True
    # (3.0, 4.0)
    # b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
    # 5.0
    # True False

    # 测试类方法.frombytes
    print('-'*20)
    v1_clone = Vecter.frombytes(octets)
    print(f'{v1!r}')
    print(v1 == v1_clone)

    # 输出
    # Vecter([3.0, 4.0])
    # True

    # 测试三维向量
    print('-'*20)
    v1 = Vecter([3,4,5])
    x,y,z = v1
    print(x,y,z)
    print(f'{v1!r}')
    v1_clone == eval(repr(v1))
    print(v1 == v1_clone)
    print(v1)
    print(abs(v1))
    print(bool(v1),bool(Vecter([0,0,0])))

    # 输出
    # 3.0 4.0 5.0
    # Vecter([3.0, 4.0, 5.0])
    # False
    # (3.0, 4.0, 5.0)
    # 7.0710678118654755
    # True False


    # 测试多维向量
    print('-'*20)
    v7 = Vecter(range(7))
    print(f'{v7!r}')
    print(abs(v7))

    # 输出
    # Vecter([0.0, 1.0, 2.0, 3.0, 4.0, ...])
    # 9.539392014169456

    # 测试__bytes__和 .frombytes() 方法
    print('-'*20)
    v1 = Vecter([3,4,5])
    v1_clone = Vecter.frombytes(bytes(v1))
    print(f'{v1_clone!r}')
    print(v1 == v1_clone)

    # 输出
    # Vecter([3.0, 4.0, 5.0])
    # True

    # 测试序列行为
    print('-'*20)
    v1 = Vecter([3,4,5])
    print(len(v1))
    print(v1[0],v1[len(v1)-1],v1[-1])

    # 输出
    # 3
    # 3.0 5.0 5.0

    # 测试切片
    print('-'*20)
    v7 = Vecter(range(7))
    print(v7[-1])
    print(v7[1:4])
    print(v7[-1:])
    # print(v7[1,2])    # TypeError: 'tuple' object cannot be interpreted as an integer

    # 输出
    # 6.0
    # (1.0, 2.0, 3.0)
    # (6.0,)


    # 测试动态属性访问
    print('-'*20)
    v7 = Vecter(range(7))
    print(v7.x)
    print(v7.y,v7.z,v7.t)

    # 输出
    # 0.0
    # 1.0 2.0 3.0

    # 动态属性查找失败情况
    print('-'*20)
    # print(v7.k)   # AttributeError: 'Vecter' 对象中没有属性 'k'
    v3 = Vecter(range(3))
    # print(v3.t)   # AttributeError: 'Vecter' 对象中没有属性 't'
    # print(v3.spam)  # AttributeError: 'Vecter' 对象中没有属性 'spam'

    # 测试哈希
    print('-'*20)
    v1 = Vecter([3,4])
    v2 = Vecter([3.1,4.2])
    v3 = Vecter([3,4,5])
    v6 = Vecter(range(6))
    print(hash(v1),hash(v2),hash(v6))

    # 输出
    # 7 384307168202284039 1


    # 测试使用format()格式化二维笛卡尔坐标系
    print('-'*20)
    v1 = Vecter([3,4])
    print(format(v1))
    print(format(v1,'.2f'))
    print(format(v1,'.3e'))

    # 输出
    # (3.0, 4.0)
    # (3.00, 4.00)
    # (3.000e+00, 4.000e+00)

    # 测试使用format()格式化三维笛卡尔坐标系
    print('-'*20)
    v3 = Vecter([3,4,5])
    print(format(v3))
    print(format(Vecter(range(7))))

    # 输出
    # (3.0, 4.0, 5.0)
    # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

    # 测试使用format()格式化二维，三维和四维球面坐标系
    print('-'*20)
    print(format(Vecter([1,1]),'h'))
    print(format(Vecter([1,1]),'.3eh'))
    print(format(Vecter([1,1]),'0.5fh'))
    print(format(Vecter([1,1,1]),'h'))
    print(format(Vecter([2,2,2]),'.3eh'))
    print(format(Vecter([0,0,0]),'0.5fh'))
    print(format(Vecter([-1,-1,-1,-1]),'h'))
    print(format(Vecter([2,2,2,2]),'.3eh'))
    print(format(Vecter([0,1,0,0]),'0.5fh'))

    # 输出
    # <1.4142135623730951, 0.7853981633974483>
    # <1.414e+00, 7.854e-01>
    # <1.41421, 0.78540>
    # <1.7320508075688772, 0.9553166181245093, 0.7853981633974483>
    # <3.464e+00, 9.553e-01, 7.854e-01>
    # <0.00000, 0.00000, 0.00000>
    # <2.0, 2.0943951023931957, 2.186276035465284, 3.9269908169872414>
    # <4.000e+00, 1.047e+00, 9.553e-01, 7.854e-01>
    # <1.00000, 1.57080, 0.00000, 0.00000>
