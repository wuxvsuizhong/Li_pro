def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None),int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'

def print_args(name,*args):
    comb_args = ','.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__({comb_args})')

class Overriding:
    def __get__(self,instance,owner):   # instance是托管实例，owner是托管类
        print_args('get',self,instance,owner)

    def __set__(self,instance,value):
        """实现了__set__方法的描述符类是覆盖性描述符"""
        print_args('set',self,instance,value)

class OverridingNoGet:
    def __set__(self,instance,value):
        """实现了__set__方法的描述符类是覆盖性描述符"""
        print_args('set',self,instance,value)


class NoOverriding:
    def __get__(self,instance,owner):
        """没有实现__set__方法的描述符类是非覆盖性描述符"""
        print_args('get',self,instance,owner)


class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NoOverriding()

    def spam(self):
        print(f'->Managed.spam({display(self)})')

if __name__ == "__main__":
    print('-'*20,"访问Overriding描述符",'-'*20)
    obj =Managed()
    # 访问属性，调用描述符类的__get__
    obj.over # -> Overriding.__get__(<Overriding object>,<Managed object>,<class Managed>)
    Managed.over # -> Overriding.__get__(<Overriding object>,None,<class Managed>) 使用的是类Managed访问类属性over，所以没有类实例instance,是None

    # 设置属性，调用描述符类的__set__
    obj.over = 7 # -> Overriding.__set__(<Overriding object>,<Managed object>,7)
    obj.over # Overriding.__get__(<Overriding object>,<Managed object>,<class Managed>) 注意：这里在上一步中通过实例obj设置了over属性，但是，再次通过实例obj获取的仍然是Overriding对象

    obj.__dict__['over'] = 8    # 这里绕过描述符的__set__，直接给实例的__dict__添加属性
    print(vars(obj))   # {'over': 8}
    obj.over    # -> Overriding.__get__(<Overriding object>,<Managed object>,<class Managed>) 通过实例去访问属性，仍然访问的是描述符的__get__方法

    Managed.over = 7    # 通过类名重新设置同名属性值，没调用__set__
    obj.over    # {'over': 8} # 通过实例访问属性，没调用__get__，但是上一步通过实例类名设置的属性值并没有生效
    Managed.over    # -> Overriding.__get__(<Overriding object>,<Managed object>,<class Managed>) 这里可以看出，即使是通过类Manage去重新设置属性值，但是获取属性的时候依然是调用的描述符类的__get__


    # 从这里的打印可以看出，当描述符类实现了__get__后，通过实例obj或者类名取访问属性的时候，都会调用描述符类的__get__,
    # 同理，描述符类实现了__set__方法，那么在通过实例obj去设置实例属性的时候，会调用描述符的__set__方法
    # 在通过实例对象obj.over=7给属性重新设置值，调用的是描述符的__set__方法，而没有像普通的实例类对象那样重新给实例obj添加数据(这也是因为描述符类的__set__里面除了打印之外，什么也没做的缘故)
    # 总结:如果描述符实现了__set__方法，那么，在通过实例给实例对象赋值的时候，不会像py默认的行为那样给实例动态的增加属性，而是调用描述符类的__set__，也就是描述符的__set__遮盖了属性的赋值行为。另一方面，即使是绕过描述符的__set__，通过实例obj.__dict__去给实例增加属性，但是通过实例obj再次去获取属性的时候，仍然是调用的描述符的__get__方法，而不会直接去访问obj.__dict__

    print('-'*20,"访问OverridingNoGet描述符",'-'*20)

    print(obj.over_no_get)  # <__main__.OverridingNoGet object at 0x000001DF0CA9A610>
    print(Managed.over_no_get)  # <__main__.OverridingNoGet object at 0x000001DF0CA9A610>
    # 和普通的属性一样，无论是通过实例obj还是通过类Managed访问，没有调用__get__,因为描述符类没有__get__方法

    obj.over_no_get = 7 # -> OverridingNoGet.__set__(<OverridingNoGet object>,<Managed object>,7)
    # 但是设置属性会调用描述符的__set__，也就是在描述符有__set__时，无法通过实例赋值修改同名属性

    print(obj.over_no_get)  # <__main__.OverridingNoGet object at 0x000001DF0CA9A610>
    # 通过obj设置的属性无效，访问属性仍然获得的描述符类实例

    obj.__dict__['over_no_get'] = 9     # 绕过描述符的__set__，给实例添加实例属性
    print(obj.over_no_get)  # 9     # 直接给市里的__dict__里面添加属性后，通过实例obj访问，可以得到__dict__中添加的属性
    obj.over_no_get = 7 # -> OverridingNoGet.__set__(<OverridingNoGet object>,<Managed object>,7)
    # 想直接通过obj添加实例属性，会调用描述符的__set__
    print(obj.over_no_get)  # 9 通过实例添加属性，调用描述符的__set__，但是描述符的__set__中除了打印，什么也没做，所以转而去获取实例的__dict__中的属性

    Managed.over_no_get = 10    # 这里通过类修改了描述符实例化的属性
    print(Managed.over_no_get)  # 10 在通过类实例访问属性，可以看到被修改了
    obj.over_no_get = 11    # 通过实例修改描述符实例化的属性
    print(obj.over_no_get)  # 11 通过实例访问属性发现也被修改了
    # 也就是，在描述符有__set__时，无法通过实例obj去覆盖实例中，由描述符实例化的属性的赋值行为，所有通过实例obj去修改描述符实例化的属性的行为，都会被描述符类的__set__拦截
    # 只有通过类名修改同名的描述符实例化的属性，才能覆盖掉描述符属性，覆盖后，如果实例中没有同名属性，那么通过实例获取的属性，就是之前通过类名覆盖的值，如果有同名的实例属性，那么获取的就是实例之前存在的实例属性


    # 总结：如果描述符类实现了__set__，那么，去设置实例属性时，都会优先调用描述符的__set__,而不是直接去操作实例去添加属性；
    # 如果描述符中没有实现__get__，那么在设置或者访问属性的时候就会调用python的默认行为。

    print('-'*20,"访问NonOverriding描述符",'-'*20)
    obj2 = Managed()
    print(vars(obj2))   # {}
    obj2.non_over   # -> NoOverriding.__get__(<NoOverriding object>,<Managed object>,<class Managed>)
    obj2.non_over = 7   # 没有调用描述符的__set__,因为没有定义，这里直接给实例obj2设置同名属性non_over
    print(obj2.non_over)    # 7 描述符实例被覆盖，没有调用描述符的__get__
    Managed.non_over    # -> NoOverriding.__get__(<NoOverriding object>,None,<class Managed>) 通过类名访问属性时仍然调用描述符的__get__，而不是直接访问实例属性
    del obj2.non_over # 删除实例属性
    print('del')
    obj2.non_over   # -> NoOverriding.__get__(<NoOverriding object>,<Managed object>,<class Managed>)
    # 恢复访问描述符的__get__

    print('-'*20,"通过类名直接覆盖类中的描述符",'-'*20)
    obj = Managed()
    Managed.over = 1
    Managed.over_no_get = 2
    Managed.non_over = 3
    print(obj.over,obj.over_no_get,obj.non_over)    # 1 2 3

    print('-'*20,"类中的函数是描述符",'-'*20)
    obj = Managed()
    print(obj.spam) # <bound method Managed.spam of <__main__.Managed object at 0x0000023DB04EA850>>
    print(Managed.spam) # <function Managed.spam at 0x0000023DB04EE520>
    obj.spam = 7
    print(obj.spam) # 7

    # 这里有一个重要的信息：通过实例obj访问apsm和通过类Managed方法spam，得到的是不同的对象
    # python的机制是——在类中定义的方法，其实在实实例上调用，就会变成绑定方法，用户自定义的函数默认都有__get__，依附到类上之后，就是描述符，但是函数没有__set__，属于非覆盖性描述符

# ##############
# 类中的方法是描述符
# ##############
import collections

class Text(collections.UserString):
    def __repr__(self):
        return f'Text({self.data})'

    def reverse(self):
        return self[::-1]

if __name__ == "__main__":
    print('-'*20,"类中的方法是描述符",'-'*20)

    word = Text('forawrd')
    print(word) # forawrd
    print(word.reverse())   # drwarof
    print(Text.reverse(Text('backword')))   # drowkcab
    print(type(Text.reverse),type(word.reverse))    # <class 'function'> <class 'method'>
    # 注意类型不同，Text.reverse得到的是function,和欧通函数相当
    # word.reverse得到的是method，和类相关

    print(list(map(Text.reverse,['repaid',(10,20,30),Text('stressed')])))   # ['diaper', (30, 20, 10), Text('desserts')] 通过类Text调用reverse方法，相当于调用普通函数

    print('Text.reverse.__get__(word):',Text.reverse.__get__(word))
    # <bound method Text.reverse of Text('forawrd')> 通过__get__方法，传入第一个参数instance，也就是实例是word，返回的是绑定方法
    print('Text.reverse.__get__(None,Text):',Text.reverse.__get__(None,Text))
    # <function Text.reverse at 0x000001A268A2E660> 通过__get__方法，传入的第一个参数如果是None(第二个参数是托管类)，那么返回的是普通函数function

    print(word.reverse) # <bound method Text.reverse of Text('forawrd')> 和调用__get__返回的是一样的
    print('word.reverse.__self__:',word.reverse.__self__)    # forawrd
    print(word.reverse.__func__ is Text.reverse)    # True 也就是通过实例访问函数的__func__属性，得到的是类的方法的引用

    # 这里证明了类的方法，是有__get__的，也就是类里面的函数，其实也是描述符，只不过没有__set__，是一种非覆盖描述符