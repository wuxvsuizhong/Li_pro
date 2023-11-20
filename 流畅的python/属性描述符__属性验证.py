# 通过描述符实类Quantity的实例来托管类的实例

class Quantity:
    def __init__(self,storage_name):
        self.storage_name = storage_name\

    def __set__(self,instance,value):   # 这里的self代表描述符实例本身，instance表示托管的实例
        """设置的是托管类的实例instance的属性"""
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

class LineItem:
    # 通过描述符实例管理类实例weight和price
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

if __name__ == "__main__":
    t = LineItem('tt',10,1.5)
    print(t.__dict__)   # {'description': 'tt', 'weight': 10, 'price': 1.5}
    print(t.__class__.weight,t.__class__.price) # <__main__.Quantity object at 0x00000204C35C8F90> <__main__.Quantity object at 0x00000204C35C9150>
    print(t.weight,t.price) # 10 1.5

    # t2 = LineItem('tt2',0,1.5)  # ValueError: weight must be > 0

# 通过描述符实例来托管类属性，在托管后，其实每一个类属性就是描述符类的实例化 这一点通过打印t.__class__.weight/price 就可以看出来，LineItem类的类属性weight和price都是Quantity的实例
# 鉴于在LineItem类属性每次实例化的时候，都要写入和类属性同名的字符串入参，如下：
#     weight = Quantity('weight')
#     price = Quantity('price')
# 而使用__set_name__ 方法，无需再入参重复的写入参数字符串，用下面的类无需再添加入参

# ##############
# 为存储属性自动命名
# ##############
class Quantity:
    def __set_name__(self, owner, name): # owner就是托管类，name就是Quantity()实例赋值的左边的变量名
        """__set_name__这个来自元类的内置方法，会自动获取在托管类owner中，Quantity()实例左边赋值的变量名"""
        self.storage_name = name

    def __set__(self,instance,value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

class LineItem:
    weight = Quantity()
    price = Quantity()
    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

# #######################
# 实现不同的属性验证(管理)方式
# #######################
# 上述的描述符实例Quantity只实现了针对属性需要>0的情况，为了能够添加其他的验证属性功能，并且能够适应更多的场景
# 先定义一个抽象基类，然后再这个抽象基类中，调用具体由其子类实现的抽象方法，为属性验证增加额外的功能
import abc

class Validated(abc.ABC):
    def __set_name__(self, owner, name):
        self.storage_name = name

    @abc.abstractmethod
    def validate(self,name,value):
        """该抽象方法由具体的子类实现功能,返回通过验证的值，或者是抛出ValueError"""
    def __set__(self,instance,value):
        value = self.validate(self.storage_name,value)
        instance.__dict__[self.storage_name] = value    # 把上一步通过方法validate验证过的之赋给托管的实例instance

class Quantity(Validated):
    """数值大于0的描述符类"""
    def validate(self,name,value):
        if value <= 0:
            raise ValueError(f'{name} must be >0')
        return value

class NonBlank(Validated):
    """数值不为空的描述符类"""
    def validate(self,name,value):
        value = value.strip()
        if not value:
            raise ValueError(f'{name} cannot be blank')
        return value

class LineItem:
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

if __name__ == "__main__":
    l1 = LineItem('',10,1.5)    # ValueError: description cannot be blank