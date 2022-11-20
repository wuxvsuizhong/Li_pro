#! /usr/bin/python

Person = type("Person", (), {"name": "unname"})
p1 = Person()
print(p1.name)

#用type创建元类的时候添加属性和方法
def func(self):
    print('added func attr')
Person2 = type("Person2",(),{"name":"unname","func":func})
p2 = Person2()
p2.func()
print(p2.name)

# type 创建元类V的形式:类名=type("类名(字符串)",(父类1,父类2,父类3,...),{"属性名1":属性值1,"属性名2":属性值2,...})

# type 创建出的类可以像正常类一样被继承

Worker = type("Worker", (Person,), {"job": "onjog"})
w1 = Worker()
print(w1.name)  # 继承父类Person的name
print(w1.job)


# metaclass 指定类的元类
def PClass(class_name, class_parent, class_attr):
    attrs = {}
    for key, val in class_attr.items():
        if not key.startswith('__'):
            attrs[key.upper()] = val

    return type(class_name, class_parent, attrs)


class MyClass(object, metaclass=PClass):    #python3中用metaclass指定类的元类
    foo = "foo"

    def addfunc(self):
        print('add function...')

m1 = MyClass()
# print(m1.foo)   #报错因为在元类PClass中已经把类的属性由小写转为大写了
print(m1.FOO)
# m1.addfunc()    #类方法也被转化成为大写
m1.ADDFUNC()


def addfuncc(self):
    print("add funcc...")

def PClass2(className,classParent,classAttr):
    attrs={}
    for key,val in classAttr.items():
        if not key.startswith("__"):
            attrs[key.upper()] = val

    attrs['addfuncc']=addfuncc     #在元类处理时动态添加类方法属性
    return type(className,classParent,attrs)

class MyClass2(object,metaclass=PClass2):
    foo2="foo2"
    def myfunc(self):
        print('myfunc ...')


mm2 = MyClass2()
# mm2.myfunc()
mm2.MYFUNC()
mm2.addfuncc()