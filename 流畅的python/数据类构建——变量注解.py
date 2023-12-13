class DemoPLainClass:
    # 常规的类中定义带类型注解的属性，都不会出现在实例属性和类属性中
    a:int # 只注解，没有赋值将无效，也无法通过在实例化时传参覆盖
    b:float = 1.1   #将被添加为类属性
    c = 'span'  # 类属性

try:
    # print(DemoPLainClass.a)  ##error a在类的定义中带注解但是没有赋初值，无法添加为类属性
    print(DemoPLainClass.b)
    print(DemoPLainClass.c)
    print(DemoPLainClass.__annotations__)  # __annotations__ 返回对象注解的参数信息

    # DP1 = DemoPLainClass(10) #error 无法传递值，a在类的定义中带注解但是没有赋初值，无法添加为类属性
    DP1 = DemoPLainClass()
    DP2 = DemoPLainClass()
    # print(DP1.a)
    print(DP1.b)
    print(DP1.c)
    print(id(DP1.b),id(DP2.b))      # 2220247394704 2220247394704 两个实例的b属性id一样，说明b是类属性
    print(id(DP1.c),id(DP2.c))      # 140720679986672 140720679986672 两个实例的b属性id一样，说明b是类属性



except Exception as e:
    print(e)
'''
总结:普通的class,添加类注解，如果不赋值，那么无法添加为类属性，只有在赋初值的时候才能被添加为类属性
注解且有赋初值的时候，可以添加为类属性，但是仍然无法再创建实例时通过传递值创建属性为实例属性
也就是说，在普通的class中的注解属性，最多只能添加为类属性
'''
print('-'*20)


import typing
# typing.NameTuple可以把添加的属性添加为类属性
class DemoNTClass(typing.NamedTuple):
    a:int
    b:float = 1.1
    c = 'span'   # 无法通过在实例化时传递赋值来覆盖

print(DemoNTClass.a)  #可以通过类名来访问到a,说明可以添加为类属性
print(DemoNTClass.b)
print(DemoNTClass.c)
print(DemoPLainClass.__annotations__)

print('-'*10)

nt = DemoNTClass(8,1.2)  #可以通过传递参数创建实例属性，但是也只是有注解的那些属性
print(nt.a)
print(nt.b)
print(DemoNTClass.b)
print(nt.c)
print('-'*20)

# 使用dataclass

from dataclasses import dataclass
@dataclass
class DemoDataClass:
    a:int         # 和普通class不同的是，经过dataclass装饰器修饰的对象，虽不能添加为类属性，但是可以实例化时通过传参来将其设置为实例属性,如果实例化的时候不传递参数而又没有设置默认值，那么实例化会报错缺少参数
    b:float = 1.1  # 有设置默认值的参数的属性，在实例化的时候，如果传递了参数，那么可以成为实例化的属性，如果没有传递参数，那么就会是类属性
    c = 'span'

# print(DemoDataClass.a)    #error 只是添加了注解没有赋值，无法添加为类属性(但是可以在构建时传入参数，创建为实例属性)
print(DemoDataClass.b)
print(DemoDataClass.c)
print(DemoPLainClass.__annotations__)

print('-'*10)
dc = DemoDataClass(9)   #使用dataclass，设置类型但是不赋值时可以通过参数传递，将属性添加为实例属性
print(dc.a)
print(dc.b)
print(dc.c)
print('-'*10)
dc2 = DemoDataClass(2.2)
print(dc2.a)
print(dc2.b)
print(dc2.c)
# dc3 = DemoDataClass(3,3.3,'good')  # TypeError: DemoDataClass无法通过传参数来覆盖c
dc4=DemoDataClass(4,4.4)  # 使用dataclass,可以在创建实例化时传递参数来覆盖有类型修饰的变量，将其创建为实例化参数
print(dc4.a)
print(dc4.b)
print(dc4.c)

# 总结：在普通的class中添加带注解的属性，如果不赋初始值，那么属性无法添加为类属性和实例属性
# 和普通的calss相比，使用dataclass装饰器时，如果添加的属性只有类型注解但是没有赋初值，也不能添加为类属性，但是可以在实例化时传参转化为实例属性。
# 使用datacalss修饰的class,如果只添加了类型注解，但是没有赋值默认值，那么必须要在实例化的时候传递参数覆盖，否则会报错缺少参数实例化失败；
# 在使用typing.NameTuple时，添加了的属性只要有类型注解，就可以添加为类属性和实例属性
# 继承了typing.NameTuple的class类型，在实例化时传递入参就可以创建实例属性,如果不传递值则使用类属性(由datacalss修饰的参数如果有定义默认值那么同样满足该规则)
# 只要是带类型注解的属性，都会在类的__annotations__中
# 直接在class定义中通过=复制的属性，无法通过实例化时传递参数来覆盖值，这样的属性被固定设置为类属性，这一点不论是普通class还是继承自typing.NameTuple，或者是使用dataclass装饰器的，都适用该规则