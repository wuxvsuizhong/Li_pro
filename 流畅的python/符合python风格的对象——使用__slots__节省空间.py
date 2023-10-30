class Pixel:
    __slots__ = ('x','y')

p = Pixel()


try:
    print(p.__dict__)   # AttributeError: 'Pixel' object has no attribute '__dict__'. Did you mean: '__dir__'?
except Exception as e:
    print(str(e))   # 'Pixel' object has no attribute '__dict__'

p.x = 10
p.y = 20
try:
    p.color = 'red'
except Exception as e:
    print(str(e))   #'Pixel' object has no attribute 'color'


# 默认情况下，python把各个实例的属性都存在一个__dict__的字典中
# 类中设置了__slots__后，类的属性将不会有__dict__
# __slots__可以是元素或者列表(只要是序列的形式)
# __slots__相比于默认的使用字段存储的字典__dict__，更加节省内存
# 设置了__dict__以后，只能设定在__slots__中有的属性，不在其中的，设置将会报错AttributeError

class OPenPixel(Pixel):
    pass

op = OPenPixel()
print(op.__dict__)  # {}
print(op.__slots__) # ('x', 'y')
op.x = 8
print(op.__dict__)  # {}
print(op.x)         # 8
op.color = 'green'
print(op.__dict__)  # {'color': 'green'}

# 如果一个类设置了__slots__，那么继承它的子类也会继承来自父类的__slots__
# 但是子类中会重新有__dict__方法，它不受父类的__slots__的影响
# 基类(父类)的__slots__属性会被添加到当前的子类的__slots__属性中
# 在子类给__slots__中的属性赋值时，赋值的属性仍然不在子类的__dict__中
# 因子类又重新有了__dict__，所以子类尅设置添加不在__slots__中的属性

class ColorPixel(Pixel):
    __slots__ = ('color',)

cp = ColorPixel()
try:
    print(cp.__dict__)
except Exception as e:
    print(str(e))   # 'ColorPixel' object has no attribute '__dict__'

cp.x = 2
cp.color = 'blue'
print(cp.__slots__)
try:
    cp.flavor = 'banana'
except Exception as e:
    print(str(e))   # 'ColorPixel' object has no attribute 'flavor'


# 当子类也添加了自己的__slots__时，那么子类的__dict__将再次不可见
# 子类设置了__dict__以后,也将只能设置__slots__中有的属性,这里的'__slots__中发的属性' 包含父类中的__slots__的
# 为了__slots__节省类的占用内存，需要每个类都定义自己的__slots__
# 设置了__slots__后，实例只能拥有__slots__中的属性，除非再次添加__dict__到__slots__中，但是这样就失去了__slots__的意义
# 有__slots__的类不能使用@cache_property装饰器，除非把__dict__加入到__slots__中
# 如果不把__weak_ref__加入到__slots__中，那么实例不能作为弱引用的目标







