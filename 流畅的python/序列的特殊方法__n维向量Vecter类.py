from array import  array
import reprlib
import math

class Vecter:
    typecode = 'd'    # 类属性

    def __init__(self,components):
        self._components = array(self.typecode,components)

    def __iter__(self):
        return iter(self._components)   # 为了使用_components，构建一个迭代器作为返回值

    def __repr__(self):
        # 被repr()方法调用
        # 使用reprlib.repr对输出的格式进行更加简洁的调整，所欲的项显示为...
        components = reprlib.repr(self._components)
        print("最初的reprlib.repr:",components)    # 最初的reprlib.repr: array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])
        components = components[components.find('['):-1]    # 截取reprlib.repr的结果，拼接自己的格式
        return f'Vecter({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (
            bytes([ord(self.typecode)])+
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
    def fromybtes(cls,octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)    # 这里不用*memv的原因是本身Vecter的类初始化__init__接受的就是可迭代的类序列components


print(Vecter([3.1,4.2]))    # (3.1, 4.2) 入参是列表类型
print(Vecter((3,4,5)))  # (3.0, 4.0, 5.0) 入参是元组类型
v1 = Vecter(range(10))
print(v1)   # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0) 入参是range可迭代序列
print(repr(v1)) # Vecter([0.0, 1.0, 2.0, 3.0, 4.0, ...])    调用__repr__自己拼接的格式

print(v1[0])    # TypeError: 'Vecter' object is not subscriptable



