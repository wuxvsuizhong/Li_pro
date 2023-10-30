from array import  array
import math

class Vecter2d:
    __match_args__ = ('x','y')  # __match_args__属性用于列出可供匹配的实例属性
    typecode = 'd'      # 转换成字节序的时候，使用8字节的双精度浮点数表示向量的想x，y分量
    
    def __init__(self,x,y):
        self.__x = float(x)
        self.__y = float(y)
    #     设置坐标值为私有属性
        
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    def __iter__(self):
        return (i for i in (self.x,self.y))
    
    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r},{!r})'.format(class_name,*self)
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode,self)))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __hash__(self):
        return hash((self.x,self.y))
    
    def __abs__(self):
        return math.hypot(self.y,self.x)
    
    def __bool__(self):
        return bool(abs(self))
    
    def angle(self):
        return math.atan2(self.y,self.x)
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self),self.angle())
            outer_fmt = '<{},{}>'
        else:
            coords = self
            outer_fmt = '({}.{})'
        components = (format(c,fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls,octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


if __name__ == "__main__":
    v1 = Vecter2d(3,4)
    print(v1.x,v1.y)    # 3.0 4.0
    x,y = v1
    print(x,y)  # 3.0 4.0
    print(v1)   # (3.0, 4.0)
    v1_clone = eval(repr(v1))
    print(v1 == v1_clone)   #True
    print(v1)   # (3.0, 4.0)
    octets =bytes(v1)
    print(octets)   # b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
    print(abs(v1))  # 5.0
    print(bool(v1),bool(Vecter2d(0,0))) # True False

    # 测试类方法frombytes
    print('-'*20,'测试类方法frombytes','-'*20)
    v1_clone = Vecter2d.frombytes(octets)
    print(v1_clone) # (3.0, 4.0)
    print(v1 == v1_clone)   # True

    # 使用笛卡尔坐标format(直角坐标系)
    print('-'*20,'使用笛卡尔坐标format(直角坐标系)','-'*20)
    print(format(v1))
    print(format(v1,'.2f'))
    print(format(v1,'.3e'))

    # 测试angle方法
    print('-'*20,'测试angle方法','-'*20)
    print(Vecter2d(0,0).angle())    #计算弧度值
    print(Vecter2d(1,0).angle())
    epsilon = 10**-8
    print(abs(Vecter2d(0,1).angle() - math.pi/2) < epsilon) #True   计算弧度值，进行比较
    print(abs(Vecter2d(1,1).angle() - math.pi/4) < epsilon) #True

    # 使用极坐标测试format
    print('-'*20,'使用极坐标测试format','-'*20)
    print(format(Vecter2d(1,1),'p'))
    print(format(Vecter2d(1,1),'.3ep'))
    print(format(Vecter2d(1,1),'0.5fp'))

    # 测试只读属性x和y
    print('-'*20,'测试只读属性x和y','-'*20)
    try:
        print(v1.x,v1.y)
        v1.x = 123
        print(v1.x,v1.y)
    except Exception as e:
        print(str(e))

    # 测试哈希
    print('-'*20,'测试哈希','-'*20)
    v1 = Vecter2d(3,4)
    v2 = Vecter2d(3.1,4.2)
    print(len({v1,v2})) # 2 v1和v2可以被放入到集合中，说明已经是可哈希的了

# ######################
# 类属性的覆盖
# ######################

if __name__ == "__main__":
    print('-'*20,'类属性的覆盖','-'*20)

    v1 = Vecter2d(1.1,2.2)
    dumped = bytes(v1)
    print(dumped)   # b'd\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@'
    print(len(dumped))      # 17
    v1.typecode = 'f'       # 设置使用4字节的单精度浮点数表示坐标x,y分量
    dumpf = bytes(v1)
    print(dumpf)        # b'f\xcd\xcc\x8c?\xcd\xcc\x0c@'  实例的typecode属性诶覆盖为'f'
    print(len(dumpf))   # 9

    print(Vecter2d.typecode) # d

    # 当实例属性和类属性有同名的属性时，实例优先使用实例的属性，类的属性被隐藏
    # Vecter2d的实例v1，重新赋值了typecode属性，那么实例的同名属性会覆盖类的同名属性
    # 在类的属性被实例的同名属性覆盖后，要访问类的属性只能通过 “类名.属性名” 访问

# #####################
# 继承然后修改基类的类属性
# #####################
class ShortVecter2d(Vecter2d):
    typecode = 'f'      # 设置使用4字节的单精度浮点数表示坐标x,y分量


if __name__ == "__main__":
    print('-'*20,'继承然后修改基类的类属性','-'*20)
    sv = ShortVecter2d(1/11,1/27)
    print(sv)
    print(len(bytes(sv)))