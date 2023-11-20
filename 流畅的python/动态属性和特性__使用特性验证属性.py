class LineItem:
    """一个无法检验属性赋值的商品类"""
    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtool(self):
        return self.weight * self.price


if __name__ == "__main__":
    raisins = LineItem("商品1",10,6.95)
    print(vars(raisins)) # {'description': '商品1', 'weight': 10, 'price': 6.95}
    # vars获取实例属性(__dict__中的内容)，此时，price，weight还是实例属性
    print(raisins.subtool())    # 69.5
    raisins.weight = -20    # 给商品的重量赋值了负数
    print(raisins.subtool())    # -139.0 这里计算总价出现了问题

class LineItem:
    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight    # 这里已经使用了@property装饰的使用特性的设置值的方法
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):   # 读取weight属性的方法
        return self.__weight    # 真正的属性放在私有属性__weight中

    @weight.setter
    def weight(self,value):     # 设置weight值的方法
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

if __name__ == "__main__":
    wal = LineItem('wal',1,-10.00)  # 没有设置price的property，所以此时为price设置小于0的值还是可以通过
    print(vars(wal)) # {'description': 'wal', '_LineItem__weight': 1, 'price': -10.0}
    # vars返回实例中的实例属性(__dict__中的内容)，可以看到，在实例属性中已经没有weight
    # 而私有属性__weight,在列出的属性列表中有_LineItem__weight
    # 可以得到的结论是，在经过property修饰后的weight，已经不再是实例属性,那么它是什么?

    wal2 = LineItem('wal2',2,1)
    print(id(wal.weight),id(wal2.weight))   # 140708948861736 140708948861768
    print(wal.weight,wal2.weight)   # 1 2


    # walnuts = LineItem('walnuts',0,10.00)   # ValueError: value must be > 0
    # 但是weight有property设置，现在如果为商品设置的weight属性是<=0的值，会报错，如果需要为跑price也设置值检验，那么同weight添加property装饰器即可

# #############
# property的原型
# #############
class LineItem:
    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):
        return self.__weight

    def set_weight(self,value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight,set_weight)
    # property函数在python2.2引入，但是在python2.4才有@语法，因此在以前的版本中，如果要定义特性，只能把存取函数传递给property函数

# if __name__ == "__main__":
#     walnuts = LineItem('walnuts',0,10.00)   # ValueError: value must be > 0

# #####################
# 进一步探究实例属性和类属性
# #####################

class Class:
    """Class 类有两个类属性 data和prop"""
    data = 'tht class data attr'
    @property
    def prop(self):
        """经过property装饰后，prop成为特性(类属性)"""
        return 'the prop value'

if __name__ == "__main__":
    obj = Class()
    print(vars(obj))    # {}    类实例中属性为空
    print(obj.prop) # the prop value    通过实例obj访问prop属性,因此时实例obj中实例属性为空，所以转而获取类属性prop
    print(obj.data) # tht class data attr   通过实例访问data属性

    obj.data = 'bar'    # 重新给实例的data属性赋值
    print(vars(obj))    # {'data': 'bar'}   此时实例有了实例属性data:bar
    print(obj.data) # bar   获取obj实例的实例属性data
    print(Class.data)   # tht class data attr   通过类名Class获取属性data，发现仍然是访问的类属性tht class data attr

    # 也就是如果实例和类属性的属性名称相同，如有同名的实例属性，那么通过实例获取的是实例属性
    # 如果想要获取同名的类属性，使用类名Classname.attr 获取类属性
    # 如果只有类属性attr而没有实例属性attr,那么通过实例obj.attr获取，和通过Class.attr获取的都是类属性

    print(Class.prop)   # <property object at 0x0000028647E74810> prop是类特性
    print(obj.prop) # the prop value 此时实例obj中只有实例属性data，所以通过实例obj去访问的仍然是类特性prop
    # obj.prop = 'foo'    # AttributeError: property 'prop' of 'Class' object has no setter

    # 解答了之前的问题，经过property修饰后的属性不是实例属性那么是什么?——prop是经过property修饰的，现在它是类特性 property object
    # prop在成为类特性后，无法直接通过实例obj.prop=’foo'赋值(因为没有setattr对应的方法)

    obj.__dict__['prop'] = 'foo' # prop成为类特性后，暂时无法通过实例obj赋值，但是可以间接通过实例的__dict__设置同名的实例属性prop
    print(vars(obj))    # {'data': 'bar', 'prop': 'foo'} 实例obj现在有两个实例属性data和prop
    print(obj.prop)     # the prop value 但是通过实例obj.prop去获取的时候，却不是直接访问的obj.__dict__中的属性，而是先访问的类特性prop
    Class.prop = 'baz'  # 重置了Class类的特性(属性)prop
    print(Class.prop)   # baz Class.prop获取的是类属性prop
    print(obj.prop)     # foo 获取的是实例属性，obj.__dict__中的内容prop

    print('-'*20,'重新设置类特性','-'*20)
    print(obj.data) # bar 注意data未经过property修饰，原来是一个普通的类属性
    # 这里因为obj实例的__dict__中有data和prop两个属性，这里通过实例obj获取的data是实例属性
    print(Class.data)   # tht class data attr 注意此时obj实例和类Class有同名的属性data，这里通过Class类名获取类属性data
    Class.data = property(lambda self: 'the "data" prop value') # 这里把原本的普通的类属性data设置为特性
    print(obj.data) # the "data" prop value data被设置为特性后，通过实例obj获取的data就是特性的值
    del Class.data
    print(obj.data) # bar 去除类特性data后，通过实例obj访问data又获取的是实例属性data

    # 在这里，在实例obj和类Class有同名属性的时候，实例obj一开始的实例属性data是bar,而通过Class.data获取的类属性是tht class data attr
    # property重新设置Class.data后，Class.data成为了类特性，再通过实例obj.data访问时，其值为特性的值：the "data" prop value
    # 在使用del删除类特性Class.data后，通过实例obj.data访问的时候，仍然是一开始的bar

# 这里梳理一下，当只有普通的类属性和实例属性时，如果有同名的类属性和实例属性attr时，实例属性会遮盖类属性，此时通过实例obj.attr访问返回的是实例属性，而这种情况下，要访问类属性只能通过 类名.attr,或者实例 obj.__class__.attr
# 有经过proprerty修饰后的attr，升级为类特性，此时如果有同名的实例属性attr，那么通过实例obj.attr访问的，依然是类特性attr，和使用 类名.attr 的效果一样，也就是这时候，同名的实例属性attr无法遮盖类特性attr。

# #############
# 定义特性工厂函数
# #############
# 上述的LineItem类，每设置一个特性都是通过添加一个property函数或者在方法上添加装饰器，下面使用工厂方法，不用在一个个的添加property关键字
def quantity(storage_name):
    def qty_getter(instance):
        """注意这里的工厂方法返回的就是类实例instance的属性"""
        return instance.__dict__[storage_name]

    def qty_setter(instance,value):
        """注意这里的工厂方法返回的就是类实例instance的属性"""
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter,qty_setter)

class LineItem:
    weight = quantity('weight')
    price = quantity('price') # quantity是一个闭包，这里其实调用的是quantity最后返回的property函数
    # 这里是把这两个都创建为了类特性

    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == "__main__":
    print('-'*20,'定义特性工厂函数','-'*20)
    m = LineItem('mm',8,13.95)
    print(m.__dict__)   # {'description': 'mm', 'weight': 8, 'price': 13.95}

    print(m.price,m.weight) # 13.95 8 这里返回的是实例的属性，本来应该是返回的类特性，但是在LieItem的类特性工厂函数中，返回的是实例instace的实行，所以这里得到的就是最终的实例属性
    print(m.__class__.price,m.__class__.weight) # <property object at 0x00000110470E4D10> <property object at 0x00000110470E4C20>

# #########
# 处理属性删除
# #########
class A:
    def __init__(self):
        self.variables = [1,2,3,4,5,6,7,8,9,0]

    @property
    def member(self):
        print('下一个成员是:')
        return self.variables[0]

    @member.deleter
    def member(self):
        m = self.variables.pop(0)
        print(f'移除{m!r}')

if __name__ == "__main__":
    print('-'*20,'处理属性删除','-'*20)

    a1 = A()
    print(a1.member)
    del a1.member
    del a1.member
    del a1.member

