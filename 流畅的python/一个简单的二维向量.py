import math
# 关于一些python中内置方法的使用

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        # 自定义Vector的打印行为形如Vector(3,4)
        return f'Vector({self.x!r},{self.y!r})'
        # 这里的x!r即使转而去调用x的__repr__方法，常见的还有x!s调用x的__str__方法，x!a调用x的__ascii__等

    def __abs__(self):
        # 向量的模
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # 自定义Vector的bool值
        # 如果Vector的模为0则返回false
        return bool(abs(self))

    def __add__(self, other):
        # 向量相加
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        # 向量相乘
        return Vector(self.x * scalar, self.y * scalar)


v = Vector(3, 4)
print("abs(v)", abs(v))  # abs调用类的__abs__
print('v*3', v * 3)  # *操作调用类的__mul__方法
print('abs(v)*3', abs(v) * 3)

v1 = Vector(2, 4)
v2 = Vector(2, 1)
print('v1+v2', v1 + v2)  # +操作调用类的__add__方法
