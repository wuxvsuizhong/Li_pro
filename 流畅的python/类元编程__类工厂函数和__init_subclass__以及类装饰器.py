# type是一个元类，是构建类的类
class MysuperClass:...
class MyMixIn:...
class MyClass(MysuperClass,MyMixIn):
    x = 42

    def x2(self):
        return self.x * 2

MyClass = type(     # 使用type构建类和使用class 定义类的效果一样
    'MyClass',      # 使用type构建的类名字符串
    (MysuperClass,MyMixIn), #继承自那些超类
    {'x':42,'x2':lambda self:self.x * 2}    # 类里面有哪些属性，方法等
)
# #############
# type是默认的元类
# #############
print(type(7))  # <class 'int'>
print(type(int))    # <class 'type'>
print(type(OSError))    # <class 'type'>
class Whatever:
    pass
print(type(Whatever))   # <class 'type'>
print(Whatever.__class__)   # <class 'type'> type()和__class__的作用相同，都是获取对象对应的类
w = Whatever()
print(w.__class__)  # <class '__main__.Whatever'>







# #########
# 类工厂函数
# #########
from typing import Union,Any
from collections.abc import Iterator,Iterable

FieldNames = Union[str,Iterable[str]]


def parse_identifiers(names:FieldNames) ->tuple[str,...]:
    if isinstance(names,str):
        names = names.replace(',',' ').split()
    if not all(s.isidentifier() for s in names):
        raise ValueError('所有的属性名必须是可用的标识符')
    return tuple(names)

def record_factory(cls_name:str,field_name:FieldNames)->type[tuple]:
    slots = parse_identifiers(field_name)

    def __init__(self,*args,**kwargs) -> None:
        attrs = dict(zip(self.__slots__,args))
        attrs.update(kwargs)
        for name,value in attrs.items():
            setattr(self,name,value)

    def __iter__(self)->Iterator[Any]:
        for name in self.__slots__:
            yield getattr(self,name)

    def __repr__(self):
        values = ','.join(f'{name} = {value!r}' for name,value in zip(self.__slots__,self))
        cls_name = self.__class__.__name__
        return f'{cls_name}({values})'

    cls_attrs = dict(
        __slots__ = slots,
        __init__ = __init__,
        __iter__ = __iter__,
        __repr__ = __repr__,
    )

    return type(cls_name,(object,),cls_attrs)

if __name__ == "__main__":
    Dog = record_factory('Dog','name weight owner')
    rex = Dog('Rex',30,'Bob')
    print(rex)  # Dog(name = 'Rex',weight = 30,owner = 'Bob')
    name,weight,_ = rex
    print(name,weight)  # Rex 30
    print("{2}'s dog weights {1}kg".format(*rex))   # Bob's dog weights 30kg

    rex.weight = 32
    print(rex)  # Dog(name = 'Rex',weight = 32,owner = 'Bob')
    print(Dog.__mro__)  # (<class '__main__.Dog'>, <class 'object'>)

# 类工厂函数的启发是，我们可以自定义实现类的方式
# #####################
# __init_subclass__的使用
# #####################
from typing import Callable,Any,NoReturn,get_type_hints
class Field:
    def __init__(self,name:str,constructor:Callable)->None:
        if not callable(constructor) or constructor is type(None):
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.constructor = constructor

    def __set__(self,instance:Any,value:Any)->None:
        if value is ...: # 如果Checked.__init__把value设置为...(内置对象Ellipsis）,就调用五参数的constructor
            value = self.constructor()
        else:
            try:
                value = self.constructor(value) # 调用有参数的constructor
            except (TypeError,ValueError) as e:
                type_name = self.constructor.__name__
                msg = f'{value!r} is not compatible with {self.name}:{type_name}'
                raise TypeError(msg) from e
        instance.__dict__[self.name]=value

class Checked:
    @classmethod
    def _fields(cls)->dict[str,type]:
        return get_type_hints(cls)  # get_type_hints时是typing模块中的一个特殊方法，可以获取对象在导入时的注解的变量名和对应变量的类型

    def __init_subclass__(subclass)->None:
        """特殊方法__init_subclass__，是一个类方法，但是不用classmethod修饰
            这个方法在定义当前类的子类时调用，第一个参数是新定义的子类(下面的子类Movie继承自Checked）
        """
        super().__init_subclass__() # 严格来说其实不用调用超类的方法
        for name,constructor in subclass._fields().items():
            setattr(subclass,name,Field(name,constructor))  #就是在这里，把属性名和属性构函数传递给描述符类Field
            # 这里给定义的子类添加属性，而这里的属性时Field描述符实例

    def __init__(self,**kwargs:Any)->None:
        for name in self._fields():
            value = kwargs.pop(name,...)
            setattr(self,name,value)
        if kwargs:
            self.__flag_unkown_attrs(*kwargs)

    def __setattr__(self, name:str, value:Any)->None:
        """一切设置实例属性的操作，会被__setattr__截获"""
        print(f'设置实例属性{name}: {value}')
        if name in self._fields():
            cls = self.__class__
            description = getattr(cls,name)
            description.__set__(self,value)
        else:
            self.__flag_unkown_attrs(name)

    def __flag_unkown_attrs(self,*names:str)->NoReturn:
        plural = 's' if len(names) > 1 else ""
        extra = ','.join(f'{name!r}' for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f'{cls_name} object has no attribute{plural} {names}')

    def _asdict(self)->dict[str,Any]:
        return {
            name:getattr(self,name) for name,attr in self.__class__.__dict__.items() if isinstance(attr,Field)
        }

    def __repr__(self)->str:
        kwargs = ','.join(f'{key}={value!r}' for key,value in self._asdict().items())
        return f'{self.__class__.__name__}({kwargs})'

class Movie(Checked):   # movie继承自Checked，在Checked构建子类Movie时， 从__init_subclass__开始
    title:str
    year:int
    box_office:float


if __name__ == "__main__":
    print('-'*20,'__init_subclass__的使用','-'*20)
    movie = Movie(title='ABC',year=2023,box_office=137)
    print(movie.title)  # ABC
    print(movie)    # Movie(title='ABC',year=2023,box_office=137.0)

    movie = Movie(title="def")
    print(movie)    # Movie(title='def',year=0,box_office=0.0)

    # block = Movie(title='Avator',year=2000,box_office='billons')
    # TypeError: 'billons' is not compatible with box_office:float

    # movie.year = 'MCMLXXII'
    # TypeError: 'MCMLXXII' is not compatible with year:int

    Movie.cvar = '类属性1' # 设置类属性不会调用__setattr__

# #####################################
# 替换__init_subclass__的方案——使用类装饰器
# #####################################
# 类装饰器是一种可调用对象，行为和函数装饰器克类似，以被装饰的类为参数，返回一个类，返回的类取代被装饰的类
def checked(cls:type)->type:
    for name,constructor in _fields(cls).items():
        setattr(cls,name,Field(name,constructor))

    cls._fields = classmethod(_fields)

    instance_mewthods = (
        __init__,
        __repr__,
        __setattr__,
        _asdict,
        __flag_unkown_attrs,
    )
    for method in instance_mewthods:
        setattr(cls,method.__name__,method)

    return cls  # 这里返回被装饰的类cls

# 下面是instance_methods中的各种方法的具体原型实现
def _fields(cls:type)->dict[str,type]:
    return get_type_hints(cls)

def __init__(self:Any,**kwargs:Any)->None:
    for name in self._fields():
        value = kwargs.pop(name,...)
        setattr(self,name,value)
    if kwargs:
        self.__flag_unkown_attrs(*kwargs)

def __setattr__(self:Any,name:str,value:Any)->None:
    if name in self._fields():
        cls = self.__class__
        descriptor = getattr(cls,name)
        descriptor.__set__(self,value)
    else:
        self.__flag_unkown_attrs(name)

def __flag_unkown_attrs(self:Any,*names:str)->NoReturn:
    plural = 's' if len(names) > 1 else ''
    extra = ','.join(f'{name}!r' for name in names)
    cls_name = repr(self.__class__.__name__)
    raise AttributeError(f'{cls_name} has no attribute{plural} P{extra}')

def _asdict(self:Any)->dict[str,Any]:
    return {
        name:getattr(self,name) for name,attr in self.__class__.__dict__.items()
        if isinstance(attr,Field)
    }

def __repr__(self:Any)->str:
    kwargs = ', '.join(f'{key}={value}' for key,value in self._asdict().items())
    return f'{self.__class__.__name__}({kwargs})'

@checked
class Movie2:
    title:str
    year:int
    box_office:float

if __name__ == "__main__":
    print('-'*20,'__init_subclass__的替代方案，使用类装饰器','-'*20)
    movie = Movie2(title='ABC',year=2023,box_office=137)
    print(movie.title)  # ABC
    print(movie)    # Movie(title='ABC',year=2023,box_office=137.0)