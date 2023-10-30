from array import array
import math


class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        """迭代Vecter2d的时候调用该方法"""
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r},{!r})'.format(class_name, *self)

    def __str__(self):
        """打印，print函数自动调用__str__方法"""
        return str(tuple(self))

    def __bytes__(self):
        """构建字节序，被bytes()函数调用"""
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self))
                )

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        """取模，被abs()函数调用。用于计算Vecter2d的模"""
        return math.hypot(self.x, self.y)

    def __bool__(self):
        """转换bool值，被bool()函数调用"""
        return bool(abs(self))  # abs(self)计算模，再转换成bool类型

    @classmethod
    def frombytes(cls, octets):
        """从字节序列构建Vecter2d实例"""
        typecode = chr(octets[0])   # 从第一个字节中拂去typecode
        memv = memoryview(octets[1:]).cast(typecode)    # 使用传入的octets字节序列创建一个memoryview，然后使用typecode进行转换
        return cls(*memv)   # 拆包转换后的memoryview，得到构造函数所需要的一对参数

    def __format__(self, format_spec=''):
        """格式化显示，被format()函数调用,可以传入格式化的字符串参数来设置格式"""
        # components = (format(c,format_spec) for c in self)  # for语句迭代会调用__iter__方法。获取Vecter2d的x,y值
        # # 这里是先迭代了Vecter2d的各个x,y值，然后分别对其x,y值的显示方式进行格式化
        # return '({},{})'.format(*components)    # 拼接组合好的格式化参数，然后返回

        if format_spec.endswith('p'):   # 极坐标的表示法
            format_spec = format_spec[:-1]
            coords = (abs(self),self.angle())   # 构建一个元祖表示极坐标
            outer_fmt = '<{}.{}>'
        else:
            coords = self   # 如果不是极坐标，那么使用self的x,y构建指教坐标
            outer_fmt = '({},{})'
        components = (format(c,format_spec) for c in coords)
        return outer_fmt.format(*components)


    def angle(self):
        """计算坐标角度"""
        return math.atan2(self.y,self.x)


v1 = Vector2d(3, 4)
print(v1.x, v1.y)  # 3.0 4.0
x, y = v1
print(x, y)  # 3.0 4.0
print(v1)  # (3.0, 4.0)
v1_clone = eval(repr(v1))
print("v1 == v1_clone", v1 == v1_clone)  # v1 == v1_clone True
print(v1)  # (3.0, 4.0)
octets = bytes(v1)
print(octets)  # b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
print(abs(v1))  # 5.0
print(bool(v1), bool(Vector2d(0, 0)))  # True False

print(format(v1))       # (3.0,4.0) 不传递格式化的参数，默认格式
print(format(v1,'.2f'))     # (3.00,4.00)   格式化的字符串.2f，也就是以两位小数显示
print(format(v1,'.3e'))     # (3.000e+00,4.000e+00)     按照科学计数法显示3位小数位

print(format(Vector2d(1,1),'p'))    # <1.4142135623730951.0.7853981633974483> 极坐标表示法
print(format(Vector2d(1,1),'.3ep')) #<1.414e+00.7.854e-01>
print(format(Vector2d(1,1),'0.5fp'))    # <1.41421.0.78540>

