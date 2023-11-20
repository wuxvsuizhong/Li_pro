# __class__用于获取对象是属于那个类
# __bases__用于获取对象的超类有那些

# 不要混淆继承关系，和数据对象的实例化关系，这是两回事
class A:
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        super().__init__()

print(int(1).__class__) # <class 'int'>
print(int.__class__)    # <class 'type'>
print(int.__bases__)    # (<class 'object'>,)

print(str('abc').__class__) # <class 'str'>
print(str.__class__)    # <class 'type'>
print(str.__bases__)    # (<class 'object'>,)



# 常规的数据对象，其归属的类都是type(实例化关系)，但是超类是object(继承关系)

a = A()
print(a.__class__)  # <class '__main__.A'>  # 实例化对象a归属的类就是类A(实例化关系)
print(A.__class__)  # <class 'type'>    # 类A本身归属的类是type，这和上面的str,int等都是一样的(实例化关系)
print(A.__bases__)  # (<class 'object'>,)   # 类A直接继承自Object，其超类是Object(继承关系)

b = B()
print(b.__class__)  # <class '__main__.B'>  # 实例化对象b，归属的类是B(实例化关系)
print(B.__class__)  # <class 'type'>    # 类对象B本身，归属属的类是type，和上面的int,str是一样的(实例化关系）
print(B.__bases__)  # (<class '__main__.A'>,)   # 类对象B继承自A，所以其超类就是类对象A(继承关系)

# 总结1：对于普通的数据对象，或者是实例化的数据对象，其归属的类就就是创建它的对应的类
# 类也是一种对象，是一种特殊的对象，也是由更高一级别的类实例化而来，也就是创建类的类，即 元类
# 元类的最终源头是type，在默认情况下，所有的对象(尤其是类对象),都是直接或者间接的是元类type的实例化

print(type.__class__)   # <class 'type'>
print(type.__bases__)   # (<class 'object'>,)
print(object.__class__) # <class 'type'>
print(object.__bases__) # ()

# 再次声明：注意，不要混淆继承关系，和实例化关系，这是两回事
# 总结2：type归属的类就是其本身，而type的超类是object，那么从这里可以得出一个结论，从继承关系上来说，object是所有对象或者是所有类的始祖类，object再向上没有超类，即便是type，也是继承自object
# object归属的类是type(注意这里说的是是实例化关系),也就是说始祖类object是type的实例化
# object和type的这种关系很微妙，但是却是python中的类延伸关系的基石，即：object是一切类，一切对象的始祖类(即使是type也是继承自object)，object再向上没有任何父类或者说超类。但是object是经过type实例化而来，而type本身是继承自object，也就是说object类是由其子类实例化得到的。
