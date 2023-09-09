class DemoPLainClass:
    # 常规的类中定义带类型注解的属性，都不会出现在实例属性中
    a:int
    b:float = 1.1   #将被添加为实例属性
    c = 'span'  # 类属性

try:
    # print(DemoPLainClass.a)  ##error a在类的定义中带注解但是没有赋初值，无法添加为实例属性
    print(DemoPLainClass.b)
    print(DemoPLainClass.c)
    print(DemoPLainClass.__annotations__)

    # DP1 = DemoPLainClass(10) #error 无法传递值，a在类的定义中带注解但是没有赋初值，无法添加为实例属性
    DP1 = DemoPLainClass()
    # print(DP1.a)
    print(DP1.b)
    print(DP1.c)

except Exception as e:
    print(e)

print('-'*20)


import typing
# typing.NameTuple可以把添加的属性添加为类属性
class DemoNTClass(typing.NamedTuple):
    a:int
    b:float = 1.1
    c = 'span'

print(DemoNTClass.a)  #可以通过类名来访问到a,说明可以添加为类属性
print(DemoNTClass.b)
print(DemoNTClass.c)
print(DemoPLainClass.__annotations__)

print('-'*10)

nt = DemoNTClass(8,1.2)  #可以通过传递参数创建实例属性
print(nt.a)
print(nt.b)
print(DemoNTClass.b)
print(nt.c)
print('-'*20)

# 使用dataclass

from dataclasses import dataclass
@dataclass
class DemoDataClass:
    a:int
    b:float = 1.1
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

# 总结：在普通的class中添加带注解的属性，如果不赋初始值，那么属性无法添加为类属性和实例属性
# 在使用typing.NameTuple时，添加了的属性只要有类型注解，就可以添加为类属性和实例属性
# 使用dataclass装饰器时，如果添加的属性只有类型注解但是没有赋初值，那么不能添加为类属性，只能添加为实例属性
# 只要是带类型注解的属性，都会在类的__annotations__中